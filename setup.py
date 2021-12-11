from setuptools import setup

setup(
   name='Restaurant_Search_Engine',
   version='1.0',
   description='Location-based search engine that uses 2 linked data datasets',
   author='Stelio Bompai-Zarogiannis Dimitrios',
   author_email='dimitriszarogiannis461@gmail.com',
   packages=['Restaurant_Search_Engine'],  #same as name
   install_requires=['SPARQLWrapper', 'typing'], #external packages as dependencies
)