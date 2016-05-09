from setuptools import setup
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(name='geppetto',
      version='0.1',
      description='Python interfaces to the Geppetto Simulation Engine',
      url='http://www.geppetto.org/',
      author='Boris Marin',
      author_email='borismarin@gmail.com',
      license='MIT',
      packages=['geppetto'])
