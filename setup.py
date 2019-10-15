import setuptools
import os


with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()


setuptools.setup(
    name='subs2vec',
    version='0.9.2',
    packages=['subs2vec'],
    package_data={
        'subs2vec': ['datasets/*/*.tsv', 'paper_results/*/*.tsv'],
    },
    author='Jeroen van Paridon & Bill Thompson',
    author_email='j.v.paridon@gmail.com',
    url='https://github.com/jvparidon/subs2vec/',
    description='subs2vec module',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'scipy',
        'pandas>=0.25',
        'lxml',
        'joblib',
        'matplotlib',
        'seaborn>=0.9',
        'scikit-learn',
        'psutil',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
