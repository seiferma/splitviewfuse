from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='splitviewfuse',
    version='0.3.0',
    description='A fuse implementation for an segmented view on a given directory.',
    long_description=long_description,
    url='https://github.com/seiferma/splitviewfuse',
    author='Stephan Seifermann',
    author_email='seiferma@t-online.de',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Filesystems',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='fuse view split segments',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['fusepy'],
    entry_points={
        'console_scripts': [
            'splitviewfuse=splitviewfuse.SplitViewFuse:main',
            'unionviewfuse=splitviewfuse.UnionViewFuse:main',
        ],
    },
)
