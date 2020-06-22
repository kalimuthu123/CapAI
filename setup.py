from setuptools import setup, find_packages

setup(
    name='capai',
    packages=['capai'],
    version='0.1',
    license='MIT',
    author='Kalimuthu',
    author_email='1995kalimuthu@gmail.com,kali@svayamlabs.com',
    url = 'https://github.com/kalimuthu123/CapAi',
    description='Convert Natural Language to SQL queries',
    keywords = ['ln2sql', 'NLP', 'SQL'],
    long_description=open('README.md').read(),
    setup_requires=['pytest'],
    package_data={
        '': ['stopwords/*.txt', 'lang_store/*.csv', 'thesaurus_store/*.dat'],
    },
)
