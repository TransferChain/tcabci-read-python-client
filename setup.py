import unittest
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name="tcabci_read_client",
    version="v0.1.0",
    author="ayhanozemre",
    description="transferchain abci read client",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayhanozemre/tcabci-read-python-client",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    test_suite='setup.test_suite'
)
