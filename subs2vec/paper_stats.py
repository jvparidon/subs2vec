import pandas as pd
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore', category=UserWarning)  # suppress annoying pandas deprecation warnings


# define convenience function for standardizing pandas Series
def standardize(Series):
    return (Series - Series.mean()) / Series.std()


# set plotting style
sns.set(context='paper', style='whitegrid', font_scale=1.0, rc={'grid.color': '.9', 'grid.linewidth': '.5'})
sns.set_palette('Set2')  # use MPI for Psycholinguistics style color palette

# data preparation
df = pd.read_csv('paper_results/model_data.tsv', sep='\t')  # load data
df = df.loc[df['vecs'] != 'wiki+subs']  # filter out wiki+subs results, we're primarily interested in wiki vs. subs here
df['wiki'] = pd.get_dummies(df['vecs'])['wiki'] - .5  # set corpus contrast to effects coding
df['analogies'] = pd.get_dummies(df['kind'])['analogies'] - (1/3)  # set task contrast to effects coding
df['norms'] = pd.get_dummies(df['kind'])['norms'] - (1/3)  # set task contrast to effects coding
df['log10_wordcount'] = np.log10(df['wordcount'])  # log-transform word counts
df['log10_wordcount_z'] = standardize(df['log10_wordcount'])  # standardize word counts


# define PyMC3 model for statistical inference
with pm.Model() as beta_model:
    # define centered Normal priors for all the betas, sd = 1 (mild shrinkage prior)
    mu = pm.Normal('β intercept', mu=0, sd=1)
    b_wordcount = pm.Normal('β corpus word count', mu=0, sd=1)
    b_wiki = pm.Normal('β corpus (mean vs. wiki)', mu=0, sd=1)
    b_norms = pm.Normal('β task (mean vs. norms)', mu=0, sd=1)
    b_analogies = pm.Normal('β task (mean vs. analogies)', mu=0, sd=1)
    b_wiki_norms = pm.Normal('β corpus (mean vs. wiki):task (mean vs. norms)', mu=0, sd=1)
    b_wiki_analogies = pm.Normal('β corpus (mean vs. wiki):task (mean vs. analogies)', mu=0, sd=1)

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
        mu
        + b_wordcount * df['log10_wordcount_z']
        + b_wiki * df['wiki']
        + b_norms * df['norms']
        + b_analogies * df['analogies']
        + b_wiki_norms * df['wiki'] * df['norms']
        + b_wiki_analogies * df['wiki'] * df['analogies']
        + mu_lang[lang_codes]
        + mu_task[task_codes]
    ))

    # define likelihood
    phi = pm.HalfNormal('φ', sd=1)  # prior for phi, for Beta(mu, phi) parametrization of the likelihood distribution
    y = pm.Beta('y', alpha=y_hat * phi, beta=(1 - y_hat) * phi, observed=df['score'])

    # sample with 3 chains, 2000 warmup + 2000 posterior samples per chain
    # target_accept was tuned to .95 to prevent occasional divergences
    trace = pm.sample(2000, tune=2000, chains=3, target_accept=.95)

# store trace summary
df_summary = pm.summary(trace, credible_interval=.9)
df_summary.to_csv('paper_results/trace_summary.tsv')
with open('paper_results/trace_summary_latex.txt', 'w') as latextable:
    latextable.write(df_summary.round(2).to_latex())

# draw and store model graph
graph = pm.model_to_graphviz(beta_model)
graph.graph_attr['rankdir'] = 'LR'  # change graph orientation to left-right (from top-down)
graph.render(filename='paper_results/model', format='pdf', cleanup=True)

# draw and store forest plot
varnames = [varname for varname in trace.varnames if 'β' in varname]  # filter out irrelevant (non-beta) parameters
pm.forestplot(trace, var_names=varnames, credible_interval=.9, figsize=(6, 4))
plt.savefig('paper_results/forestplot.pdf')
plt.savefig('paper_results/forestplot.png', dpi=600)
plt.clf()

# draw and store trace plot
pm.traceplot(trace)
plt.savefig('paper_results/traceplot.pdf')
plt.savefig('paper_results/traceplot.png', dpi=600)
plt.clf()
