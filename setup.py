import os
import sys
from setuptools import find_packages, setup

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def relative_path(path, base_dir=PACKAGE_ROOT):
    return os.path.join(base_dir, path)


requirements = []
if sys.version_info[:2] == (3, 4):
    requirements = ['typing']

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'Indented Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries',
]

test_requirements = ['tox>=2.9.1']
setup_requirements = ['setuptools-scm']


def readme():
    with open(relative_path('README.rst'), 'r') as f:
        return f.read()


setup(
    author='Nickolas Fox',
    author_email='tarvitz@blacklibrary.ru',
    url="https://github.com/tarvitz/rtquery",
    name='rtquery',
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    classifiers=classifiers,
    description='Request Tracker Querying Library',
    long_description=readme(),
    keywords='request tracker query lib',
    python_requires='>=3',
    packages=find_packages(),
    platforms=['any'],
    include_package_data=True,
    zip_safe=False,
    use_scm_version={
        'write_to': 'rtquery/_version.py',
    }
)
