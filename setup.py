
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='mobilitydb-sqlalchemy',
    version='0.3',
    description='MobilityDB extensions to SQLAlchemy',
    python_requires='>=3.7',
    project_urls={"documentation": "https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/", "homepage": "https://github.com/adonmo/mobilitydb-sqlalchemy", "repository": "https://github.com/adonmo/mobilitydb-sqlalchemy"},
    author='B Krishna Chaitanya',
    author_email='bkchaitan94@gmail.com',
    license='MIT',
    keywords='geo gis postgres mobilitydb sqlalchemy orm',
    classifiers=['Development Status :: 3 - Alpha', 'Environment :: Plugins', 'Operating System :: OS Independent', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Intended Audience :: Developers', 'Intended Audience :: Information Technology', 'Intended Audience :: Science/Research', 'License :: OSI Approved :: MIT License', 'Natural Language :: English', 'Topic :: Database :: Database Engines/Servers', 'Topic :: Scientific/Engineering :: GIS'],
    packages=['mobilitydb_sqlalchemy', 'mobilitydb_sqlalchemy.types'],
    package_dir={"": "."},
    package_data={},
    install_requires=['geoalchemy2==0.*,>=0.8.4', 'pandas==1.*,>=1.1.0', 'pymeos==0.*,>=0.1.0', 'shapely==1.*,>=1.7.0', 'sqlalchemy==1.*,>=1.3.18'],
    dependency_links=['git+https://github.com/anitagraser/movingpandas@f1f56f263ab088ae6d1c6af9a181c0a8ea3d7ab4#egg=movingpandas'],
    extras_require={"dev": ["black==19.*,>=19.10.0.b0", "dephell==0.*,>=0.8.3", "fissix==20.*,>=20.5.1", "pre-commit==2.*,>=2.6.0", "psycopg2==2.*,>=2.8.5", "pytest==6.*,>=6.0.1"], "docs": ["sphinx==2.*,>=2.3.1", "sphinx-rtd-theme==0.*,>=0.4.3", "tomlkit==0.*,>=0.5.8"], "movingpandas": ["movingpandas"]},
)
