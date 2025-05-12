from setuptools import setup

setup(
    name='ai-commiter',
    version='0.1.0',
    py_modules=['hook'],
    entry_points={
        'console_scripts': ['ai-commiter=hook:main'],
    },
)