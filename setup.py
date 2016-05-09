from setuptools import setup
from codecs import open

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(name='geppetto',
      version='0.1',
      description='Python interfaces to the Geppetto Simulation Engine',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Intended Audience :: Science/Research'
      ],
      keywords='science simulation biology bio-informatics',
      url='http://www.geppetto.org/',
      author='Boris Marin',
      author_email='borismarin@gmail.com',
      license='MIT',
      packages=['geppetto'],
      install_requires=['toposort'])
