import distutils.core

distutils.core.setup(
    name='subs2vec',    
    version='0.9.1',
    description='subs2vec module',
    author='Jeroen van Paridon & Bill Thompson',
    author_email='jvparidon@gmail.com',
    url='https://github.com/jvparidon/subs2vec/',
    packages=['subs2vec'],
    package_data={'subs2vec': ['datasets/*/*.tsv']},
)
