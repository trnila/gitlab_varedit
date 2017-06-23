from setuptools import setup, find_packages

setup(
    name='gitlab_varedit',
    packages=find_packages(),
    install_requires='python-gitlab==0.21.2',
    entry_points={
        'console_scripts': ['gitlab_varedit = gitlab_varedit.__main__:main']
    }
)