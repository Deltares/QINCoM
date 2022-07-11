#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = []

test_requirements = []

setup(
    author="Jurjen de Jong",
    author_email='jurjen.dejong@deltares.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tool for quickly computing the costs of inland shipping due to limited navigational depth",
    entry_points={
        'console_scripts': [
            'qincm=qincm.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='qincm',
    name='qincm',
    packages=find_packages(include=['qincm', 'qincm.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jurjendejong/qincm',
    version='0.1.0',
    zip_safe=False,
)
