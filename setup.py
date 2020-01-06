from setuptools import setup
from os import path
import re

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = re.search(r'^__version__\s*=\s*"(.*)"',
                    open('kacl/__init__.py').read(),
                    re.M).group(1)

setup(name='python-kacl',
      version=version,
      description='Pyhton module and CLI tool for validating and modifying Changelogs in "keep-a-changelog" format"',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/mschmieder/python-kacl',
      author='Matthias Schmieder',
      author_email='schmieder.matthias@gmail.com',
      entry_points={
           "console_scripts": ['kacl-cli = kacl.kacl_cli:start']
      },
      license='MIT',
      packages=['kacl'],
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
          'click',
          'semver',
          'pychalk',
          'gitpython',
          'pyyaml',
          'python-box'
      ],
      zip_safe=False,
      classifiers= [
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Version Control"
      ])
