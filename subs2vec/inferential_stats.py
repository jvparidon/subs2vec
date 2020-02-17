import pandas as pd
import numpy as np
import pymc3 as pm
from bambi import Model
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import logit
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Greek alphabet unicode: Α α, Β β, Γ γ, Δ δ, Ε ε, Ζ ζ, Η η, Θ θ, Ι ι, Κ κ, Λ λ, Μ μ, Ν ν, Ξ ξ, Ο ο, Π π, Ρ ρ, Σ σ/ς, Τ τ, Υ υ, Φ φ, Χ χ, Ψ ψ, and Ω ω.
# tilde: \u0303
# hat: \u0302

def standardize(Series):
    return (Series - Series.mean()) / Series.std()


plt.style.use('seaborn-whitegrid')
sns.set_palette('Set2')

df = pd.read_csv('paper_results/glmm_data.tsv', sep='\t')
df = df.loc[df['vecs'] != 'wiki+subs']
df['wiki'] = pd.get_dummies(df['vecs'])['wiki'] - .5
df['analogies'] = pd.get_dummies(df['kind'])['analogies'] - (1/3)
df['norms'] = pd.get_dummies(df['kind'])['norms'] - (1/3)
df['log10_wordcount'] = np.log10(df['wordcount'])
df['log10_wordcount_z'] = standardize(df['log10_wordcount'])


'''
model = Model(df)
results = model.fit(
    'score ~ log10_wordcount + wiki',
    random=['1|kind'],
    samples=2000, tune=2000, chains=3
)
'''

'''
df['score'] = logit(df['score'])
model = Model(df)
results = model.fit(
    'score ~ log10_wordcount + wiki * analogies + wiki * norms',
    random=['1|lang'],
    samples=2000, tune=2000, chains=3
)
graph = pm.model_to_graphviz(model.backend.model)
graph.graph_attr['rankdir'] = 'LR'
graph.render(filename='paper_results/model', format='pdf', cleanup=True)
'''

'''
pm.traceplot(model.backend.trace)
plt.savefig('paper_results/traceplot.pdf')
plt.savefig('paper_results/traceplot.png', dpi=600)
print(results.summary(ranefs=True).round(2))
'''

'''
with pm.Model() as beta_model:
    b_intercept = pm.Normal('intercept', mu=0, sd=10)
    b_wordcount = pm.Normal('log10_wordcount', mu=0, sd=1)
    b_wiki = pm.Normal('corpus (subs vs wiki)', mu=0, sd=1)
    b_norms = pm.Normal('task (sims vs norms)', mu=0, sd=1)
    b_analogies = pm.Normal('task (sims vs analogies)', mu=0, sd=1)
    b_wiki_norms = pm.Normal('corpus:task (sims vs norms)', mu=0, sd=1)
    b_wiki_analogies = pm.Normal('corpus:task (sims vs analogies)', mu=0, sd=1)

    lang_codes, lang_uniques = df['lang'].factorize()
    lang_offset = pm.Normal('lang_offset', mu=0, sd=1, shape=len(lang_uniques))
    lang_sd = pm.HalfNormal('lang_sd', sd=1)
    s_lang = pm.Deterministic('lang', lang_offset * lang_sd)

    y_est = pm.Deterministic('y_est', pm.math.invlogit(
        b_intercept
        + b_wordcount * df['log10_wordcount_z']
        + b_wiki * df['wiki']
        + b_norms * df['norms']
        + b_analogies * df['analogies']
        + b_wiki_norms * df['wiki'] * df['norms']
        + b_wiki_analogies * df['wiki'] * df['analogies']
        + s_lang[lang_codes]
    ))
    sd_beta = pm.Beta('sd_untransformed', alpha=1, beta=2)
    sd = pm.Deterministic('sd_det', pm.math.sqrt(y_est * (1 - y_est)) * sd_beta)

    y_like = pm.Beta('y_like', mu=y_est, sd=sd, observed=df['score'])
    trace = pm.sample(2000, tune=2000, chains=3)
'''

with pm.Model() as beta_model:
    mu = pm.Normal('β intercept', mu=0, sd=10)
    b_wordcount = pm.Normal('β corpus word count', mu=0, sd=1)
    b_wiki = pm.Normal('β corpus (subs vs. wiki)', mu=0, sd=1)
    b_norms = pm.Normal('β task (sims vs. norms)', mu=0, sd=1)
    b_analogies = pm.Normal('β task (sims vs. analogies)', mu=0, sd=1)
    b_wiki_norms = pm.Normal('β corpus:task (sims vs. norms)', mu=0, sd=1)
    b_wiki_analogies = pm.Normal('β corpus:task (sims vs. analogies)', mu=0, sd=1)

    task_codes, task_uniques = df['source'].factorize()
    mu_tilde_task = pm.Normal('μ\u0303 task', mu=0, sd=1, shape=len(task_uniques))
    sigma_task = pm.HalfNormal('σ task', sd=1)
    mu_task = pm.Deterministic('μ task', sigma_task * mu_tilde_task)

    lang_codes, lang_uniques = df['lang'].factorize()
    mu_tilde_lang = pm.Normal('μ\u0303 lang', mu=0, sd=1, shape=len(lang_uniques))
    sigma_lang = pm.HalfNormal('σ lang', sd=1)
    mu_lang = pm.Deterministic('μ lang', sigma_lang * mu_tilde_lang)

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
    phi = pm.HalfNormal('φ', sd=1)
    y = pm.Beta('y', alpha=y_hat * phi, beta=(1 - y_hat) * phi, observed=df['score'])

    trace = pm.sample(2000, tune=2000, chains=3, target_accept=.95)

#print(pm.summary(trace, credible_interval=.9).round(2).to_markdown())

print('creating model graph')
graph = pm.model_to_graphviz(beta_model)
graph.graph_attr['rankdir'] = 'LR'
graph.render(filename='paper_results/model', format='pdf', cleanup=True)

print('creating forest plot')
print(trace.varnames)
varnames = [varname for varname in trace.varnames if 'β' in varname]
pm.forestplot(trace, var_names=varnames, credible_interval=.9)
plt.savefig('paper_results/forestplot.pdf')
plt.savefig('paper_results/forestplot.png', dpi=600)
plt.clf()

print('creating traceplot')
pm.traceplot(trace)
plt.savefig('paper_results/traceplot.pdf')
plt.savefig('paper_results/traceplot.png', dpi=600)
plt.clf()
