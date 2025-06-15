from setuptools import setup, find_packages

setup(
    name="hbnb",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'flask==2.3.2',
        'flask-restx==1.1.0',
        'pytest==7.4.0'
    ],
)
