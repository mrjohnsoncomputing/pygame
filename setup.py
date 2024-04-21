from setuptools import setup, find_packages

setup(
    name='pygame_games',
    version='0.0.8',
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pygame',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'apple_catch = apple_catch.apple_catch.cli:test',
        ],
    },
)