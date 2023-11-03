from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="tcabci_read_client",
    version="v0.1.8",
    author="transferchain",
    description="transferchain abci read client",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/transferchain/tcabci-read-python-client",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
