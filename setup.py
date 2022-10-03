#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wedotech-tap-deliveree',
      version='0.0.1',
      description='Singer.io tap for extracting data from Deliveree Reporting API - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ashley G Ramdass <ashley@wedotech.co>',
      url='https://github.com/wedotech-limited/wedotech-tap-deliveree',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['tap_deliveree'],
      install_requires=[
          'pipelinewise-singer-python==1.3.0',
          'requests==2.28.1',
          'backoff==1.10.0'
      ],
      extras_require={
          'test': [
              'pylint==2.15.3',
              'pytest==7.1.3'
          ]
      },
      entry_points='''
          [console_scripts]
          tap-deliveree=tap_deliveree:main
      ''',
      packages=['tap_deliveree'],
      package_data={
          'tap_deliveree': ['schemas/*.json']
      },
      include_package_data=True
)