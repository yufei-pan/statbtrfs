import setuptools
from setuptools import setup
from statbtrfs import version

classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: POSIX :: Linux',
]
# setuptools 77+ (PEP 639) takes an SPDX license expression and warns about license classifiers (an error next to an
# expression); older ones (the newest for Python 3.8 and earlier, so all a Python 3.6 install has) know only the
# free-text license and the classifier. Their sdist and wheel take LICENSE by its name (setuptools 56+, wheel 0.32+).
if int(setuptools.__version__.split('.')[0]) >= 77:
    license_metadata = {'license_expression': 'GPL-3.0-or-later', 'license_files': ['LICENSE']}
else:
    license_metadata = {'license': 'GPL-3.0-or-later'}
    classifiers.append('License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)')

setup(
    name='statbtrfs',
    version=version,
    description='Query Btrfs filesystem status',
    long_description=open('README.txt', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    author='Yufei Pan',
    author_email='pan@zopyr.us',
    url='https://github.com/yufei-pan/statbtrfs',
    py_modules=['statbtrfs'],
    entry_points={
        'console_scripts': [
            'statbtrfs=statbtrfs:main',
        ],
    },
    # No multiCMD: statbtrfs carries its own copy (the embedded block in statbtrfs.py) and runs it wherever an installed one
    # is older than that copy, missing or does not import, so a requirement would guarantee nothing; and pip 9 (stock on
    # EL7 and EL8) upgrading an old multiCMD for it stopped `pip3 install -U statbtrfs` (docs/lessons.md, 2026-11-14).
    extras_require={
        'completion': [
            'argcomplete',
        ],
    },
    classifiers=classifiers,
    python_requires='>=3.6',
    **license_metadata
)
