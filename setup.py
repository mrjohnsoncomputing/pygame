from setuptools import setup

setup(
    name='pygame',
    version='0.0.1',
    py_modules=['applecatch'],
    install_requires=[
        'click',
        'pygame'
    ],
    entry_points={
        'console_scripts': [
            'yourscript = yourscript:cli',
        ],
    },
)