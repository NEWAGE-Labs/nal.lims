# -*- coding: utf-8 -*-
"""Installer for the nal.lims package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='nal.lims',
    version='1.1',
    description="A Plone Addon to change a Senaite LIMS site into a NEW AGE Laboratories LIMS site",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Paul VanderWeele',
    author_email='PVanderWeele@newagelaboratories.com',
    url='https://github.com/NEWAGE-Labs/nal.lims',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/nal.lims',
        'Source': 'https://github.com/NEWAGE-Labs/nal.lims',
        'Tracker': 'https://github.com/NEWAGE-Labs/nal.lims/issues',
        # 'Documentation': 'https://nal.lims.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['nal'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
        'senaite.core>=2.0',
        'senaite.lims>=2.0',
        'senaite.impress>=2.0',
        'senaite.jsonapi',
        'pandas==0.24.2',
        'numpy==1.16.6',
        'pyodbc',
        #'Products.PDBDebugMode',
        #'ipdb'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = nal.lims.locales.update:update_locale
    """,
)
