"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from watches import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=watches', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'watches',
    version = __version__,
    description = 'An Elasticsearch command line tool in Python.',
    long_description = long_description,
    url = 'https://github.com/lukas-vlcek/watches-cli',
    author = 'Lukas Vlcek',
    author_email = 'lukas.vlcek@gmail.com',
    license = 'ASL2',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Apache Software License v2',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'elasticsearch', 'datetime', 'logging'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'watches=watches.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
