"""Fits a Bayesian multilevel Beta regression and generates graphs/plots/tables as reported in Van Paridon & Thompson (2020)."""
import os
import pandas as pd
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore', category=UserWarning)  # suppress some annoying future deprecation warnings
path = os.path.dirname(__file__)

# set plotting style
sns.set(context='paper', style='whitegrid', font_scale=1.0, rc={'grid.color': '.9', 'grid.linewidth': '.5'})
sns.set_palette('Set2')  # use MPI for Psycholinguistics style color palette


def standardize(Series):
    """Convenience function for standardizing a pandas Series.

    :param Series: numerical pandas Series
    :return: standardized pandas Series
    """
    return (Series - Series.mean()) / Series.std()


def sum_contrast(value, target, reference):
    """Convenience function for creating sum-coded contrasts.

    :param value: value to convert into 1, 0, or -1
    :param target: target (will be recoded to 1)
    :param reference: reference (will be recoded to -1)
    :return: recoded value
    """
    if value == target:
        return 1
    elif value == reference:
        return -1
    else:
        return 0


def _fit_model():
    # data preparation
    df = pd.read_csv(os.path.join(path, 'paper_results', 'model_data.tsv'), sep='\t')  # load data
    df['log10_wordcount'] = np.log10(df['wordcount'])  # log-transform word counts
    df['log10_wordcount_z'] = standardize(df['log10_wordcount'])  # standardize word counts

    # create sum-coded contrasts
    df['wiki'] = df['vecs'].apply(lambda x: sum_contrast(x, 'wiki', 'wiki+subs'))
    df['subs'] = df['vecs'].apply(lambda x: sum_contrast(x, 'subs', 'wiki+subs'))
    df['analogies'] = df['kind'].apply(lambda x: sum_contrast(x, 'analogies', 'similarities'))
    df['norms'] = df['kind'].apply(lambda x: sum_contrast(x, 'norms', 'similarities'))

    # define PyMC3 model for statistical inference
    with pm.Model() as beta_model:
        # define centered Normal priors for all the betas, sd = 1 (mild shrinkage prior)
        b_intercept = pm.Normal('β intercept', mu=0, sd=1)
        b_wordcount = pm.Normal('β corpus word count', mu=0, sd=1)
        b_wiki = pm.Normal('β wiki vs. mean', mu=0, sd=1)
        b_subs = pm.Normal('β subs vs. mean', mu=0, sd=1)
        b_norms = pm.Normal('β norms vs. mean', mu=0, sd=1)
        b_analogies = pm.Normal('β analogies vs. mean', mu=0, sd=1)
        b_wiki_norms = pm.Normal('β wiki vs. mean:norms vs. mean', mu=0, sd=1)
        b_wiki_analogies = pm.Normal('β wiki vs. mean:analogies vs. mean', mu=0, sd=1)
        b_subs_norms = pm.Normal('β subs vs. mean:norms vs. mean', mu=0, sd=1)
        b_subs_analogies = pm.Normal('β subs vs. mean:analogies vs. mean', mu=0, sd=1)

        b_wikisubs = pm.Deterministic('β wiki+subs vs. mean', -1 * (b_subs + b_wiki))
        b_similarities = pm.Deterministic('β similarities vs. mean', -1 * (b_analogies + b_norms))
        b_wikisubs_norms = pm.Deterministic('β wiki+subs vs. mean:norms vs. mean', -1 * (b_subs_norms + b_wiki_norms))
        b_wikisubs_analogies = pm.Deterministic('β wiki+subs vs. mean:analogies vs. mean', -1 * (b_subs_analogies + b_wiki_analogies))
        b_subs_similarities = pm.Deterministic('β subs vs. mean:similarities vs. mean', -1 * (b_subs_analogies + b_subs_norms))
        b_wiki_similarities = pm.Deterministic('β wiki vs. mean:similarities vs. mean', -1 * (b_wiki_analogies + b_wiki_norms))

        # given the above, there are two ways to compute the interaction wiki+subs vs.mean:similarities vs. mean
        # both methods are given below, but we only need to use one
        # they give the exact same answer though, you can uncomment the second line to verify
        b_wikisubs_similarities = pm.Deterministic('β wiki+subs vs. mean:similarities vs. mean', -1 * (b_wiki_similarities + b_subs_similarities))
        # b_wikisubs_similarities2 = pm.Deterministic('β wiki+subs vs. mean:similarities vs. mean (2)', -1 * (b_wikisubs_analogies + b_wikisubs_norms))

        # non-centered parametrization for task-level random intercepts
        task_codes, task_uniques = df['source'].factorize()  # get number of unique groups and code them
        mu_tilde_task = pm.Normal('μ\u0303 task', mu=0, sd=1, shape=len(task_uniques))  # prior for task group offsets
        sigma_task = pm.HalfNormal('σ task', sd=1)  # prior for task group sigma
        mu_task = pm.Deterministic('μ task', sigma_task * mu_tilde_task)  # task group means (random intercepts)

        # non-centered parametrization for language-level random intercepts
        lang_codes, lang_uniques = df['lang'].factorize()  # get number of unique groups and code them
        mu_tilde_lang = pm.Normal('μ\u0303 lang', mu=0, sd=1, shape=len(lang_uniques))  # prior for lang group offsets
        sigma_lang = pm.HalfNormal('σ lang', sd=1)  # prior for lang group sigma
        mu_lang = pm.Deterministic('μ lang', sigma_lang * mu_tilde_lang)  # lang group means (random intercepts)

        # compute predictions for y, using logit link function
        y_hat = pm.Deterministic('ŷ', pm.math.invlogit(
            b_intercept
            + b_wordcount * df['log10_wordcount_z']
            + b_wiki * df['wiki']
            + b_subs * df['subs']
            + b_norms * df['norms']
            + b_analogies * df['analogies']
            + b_wiki_norms * df['wiki'] * df['norms']
            + b_wiki_analogies * df['wiki'] * df['analogies']
            + b_subs_norms * df['subs'] * df['norms']
            + b_subs_analogies * df['subs'] * df['analogies']
            + mu_lang[lang_codes]
            + mu_task[task_codes]
        ))

        # define likelihood
        phi = pm.HalfNormal('φ', sd=1)  # prior for phi, for Beta(mu, phi) parametrization of the likelihood distribution
        y = pm.Beta('y', alpha=y_hat * phi, beta=(1 - y_hat) * phi, observed=df['score'])

        # sample with 3 chains, 2000 warmup + 4000 posterior samples per chain
        # target_accept was tuned to .95 to prevent occasional divergences
        trace = pm.sample(2500, tune=2500, chains=4, target_accept=.95)

    # store trace summary as tsv and LaTeX table
    df_summary = pm.summary(trace, credible_interval=.9)
    df_summary.to_csv('trace_summary.tsv', sep='\t')
    with open('trace_summary_latex.txt', 'w') as latextable:
        latextable.write(df_summary.round(2).to_latex())

    # draw and store model graph
    graph = pm.model_to_graphviz(beta_model)
    graph.graph_attr['rankdir'] = 'LR'  # change graph orientation to left-right (from top-down)
    graph.render(filename='model', format='pdf', cleanup=True)

    # draw and store forest plot
    varnames = sorted([varname for varname in trace.varnames if ('β' in varname)])
    varnames = [
        'β intercept',
        'β corpus word count',
        'β subs vs. mean',
        'β wiki vs. mean',
        'β wiki+subs vs. mean',
        'β analogies vs. mean',
        'β norms vs. mean',
        'β similarities vs. mean',
        'β subs vs. mean:analogies vs. mean',
        'β subs vs. mean:norms vs. mean',
        'β subs vs. mean:similarities vs. mean',
        'β wiki vs. mean:analogies vs. mean',
        'β wiki vs. mean:norms vs. mean',
        'β wiki vs. mean:similarities vs. mean',
        'β wiki+subs vs. mean:analogies vs. mean',
        'β wiki+subs vs. mean:norms vs. mean',
        'β wiki+subs vs. mean:similarities vs. mean',
    ]
    axes = pm.forestplot(trace, var_names=varnames, credible_interval=.9, combined=True, figsize=(4, 6))
    axes[0].set(title='90% credible intervals', xlabel='coefficient (in log-odds)')
    plt.savefig('forestplot.pdf')
    plt.savefig('forestplot.png', dpi=600)
    plt.clf()

    # draw and store trace plot
    pm.traceplot(trace)
    plt.savefig('traceplot.png', dpi=300)  # the traceplot is huge, so we lower the resolution and don't store it as pdf
    plt.clf()

    return df_summary


if __name__ == '__main__':
    print(_fit_model())
