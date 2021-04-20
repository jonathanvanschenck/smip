import os
from setuptools import setup, find_packages


def read(fp):
    with open(os.path.join(os.path.dirname(__file__), fp)) as f:
        return f.read()

setup(
    name='smip',
    version='0.1.0',
    description='Render local markdown files, with scripture references automatically scraped from the web.',
    long_description=read('README.md'),
    author='Jonathan D B Van Schenck',
    author_email='vanschej@oregonstate.edu',
    url='http://github.com/jonathanvanschenck/smip',
    license='MIT',
    packages=find_packages(),
    package_data={'smip' : ['static/*.*', 'templates/*']},
    install_requires=read("requirements.txt").splitlines(),
    extra_requires = {'tests' : read('requirements-test.txt').splitlines()},
    zip_safe=False,
    entry_points={'console_scripts': ['smip = smip.cli:smip']}
)
