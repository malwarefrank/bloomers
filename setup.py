from setuptools import setup

setup(
    name='bloomers',
    version='0.5.0',
    py_modules=['bloomers'],
    entry_points={
        'console_scripts': ['bloomers=bloomers.app:cli'],
    },
    install_requires=[
        'pybloom_live',
    ],
    packages=['bloomers'],
)
