from setuptools import setup

setup(
    name='mtirc',
    version='1.0.0',
    author='Kunal Mehta',
    author_email='legoktm@gmail.com',
    packages=['mtirc'],
    url='http://github.com/legoktm/mtirc/',
    license='LICENSE.txt',
    description='A fully functioning multi-threaded IRC client.',
    long_description=open('README.rst').read(),
    install_requires=[
        "irc >= 8.3",
        "simplejson",
    ],
)
