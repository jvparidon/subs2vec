import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

'''
df = sns.load_dataset('iris')
#sns.jointplot(x=df["sepal_length"], y=df["sepal_width"], kind='kde')
sns.set_context('notebook')
sns.set_style('darkgrid')
g = sns.FacetGrid(df, hue='species')
g.map(sns.kdeplot, 'petal_width', 'petal_length', shade=True, alpha=.7, shade_lowest=False)
#g.map(sns.kdeplot, 'sepal_width', 'sepal_length', shade=True, alpha=.7, shade_lowest=False)
g.add_legend()
plt.savefig('density.pdf')

'''

iris = sns.load_dataset('iris')
#sns.jointplot(x=df["sepal_length"], y=df["sepal_width"], kind='kde')
sns.set_context('notebook')
sns.set_style('darkgrid')
sns.set_color_codes('muted')
g = sns.PairGrid(iris, hue='species', palette=['b', 'g', 'm'], hue_kws={'cmap': ['Blues', 'Greens', 'Purples']})
g.map_upper(sns.kdeplot, shade=True, alpha=.6, shade_lowest=False, cmap='species')
g.map_diag(sns.kdeplot, alpha=.6)
g.map_lower(plt.scatter, alpha=.6)
g.add_legend()
plt.savefig('density.pdf')
