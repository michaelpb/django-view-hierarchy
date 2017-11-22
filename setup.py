#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_view_hierarchy/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_view_hierarchy", "__init__.py")


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'test':
    os.system('py.test')
    sys.exit()


#if sys.argv[-1] == 'publish':
#    try:
#        import wheel
#        print("Wheel version: ", wheel.__version__)
#    except ImportError:
#        print('Wheel library missing. Please run "pip install wheel"')
#        sys.exit()
#    os.system('python setup.py sdist upload')
#    os.system('python setup.py bdist_wheel upload')
#    sys.exit()
#
#if sys.argv[-1] == 'tag':
#    print("Tagging the version on git:")
#    os.system("git tag -a %s -m 'version %s'" % (version, version))
#    os.system("git push --tags")
#    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django_view_hierarchy',
    version=version,
    description="""Hierarchical view system Python Django with breadcrumbs""",
    long_description=readme + '\n\n' + history,
    author='michaelb',
    author_email='michaelpb@gmail.com',
    url='https://github.com/michaelpb/django-view-hierarchy',
    packages=[
        'django_view_hierarchy',
    ],
    include_package_data=True,
    install_requires=[],
    license="GNU General Public License v3 or later (GPLv3+)",
    zip_safe=False,
    keywords='django_view_hierarchy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
    ],
)
