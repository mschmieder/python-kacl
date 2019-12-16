from setuptools import setup

setup(name='python-kacl',
      version='0.1',
      description='Pyhton module and CLI tool for validating and modifying Changelogs in "keep-a-changelog" format"',
      url='http://github.com/mschmieder/python-kacl',
      author='Matthias Schmieder',
      author_email='schmieder.matthias@gmail.com',
      license='MIT',
      packages=['pykacl'],
      scripts=['bin/kacl-cli'] ,
      zip_safe=False)