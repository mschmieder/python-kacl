from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='python-kacl',
      version='0.1.0',
      description='Pyhton module and CLI tool for validating and modifying Changelogs in "keep-a-changelog" format"',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/mschmieder/python-kacl',
      author='Matthias Schmieder',
      author_email='schmieder.matthias@gmail.com',
       entry_points = {
        "console_scripts": ['kacl-cli = kacl.kacl_cli:start']
      },
      license='MIT',
      packages=['kacl'],
      install_requires=[
        'click',
        'semver',
        'pychalk'
      ],
      zip_safe=False)