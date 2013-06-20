from setuptools import setup

setup(
    name='mtirc',
    version='0.2.1',
    author='Kunal Mehta',
    author_email='legoktm@gmail.com',
    packages=['mtirc'],
    url='http://github.com/legoktm/mtirc/',
    license='MIT License',
    description='A fully functioning multi-threaded IRC client.',
    long_description=open('README.rst').read(),
    install_requires=[
        "irc >= 8.3",
        "simplejson",
        "six",
    ],
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 2",
#                 "Programming Language :: Python :: 3",
                 "Development Status :: 2 - Pre-Alpha",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
    ],
    test_suite='tests',
)
