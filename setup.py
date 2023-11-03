from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

requirements = [
    'requests==2.31.0',
    'websockets==11.0.3',
    'websocket-client==1.6.3'
]

setup(
    name="tcabci_read_client",
    version="v0.1.9",
    author="transferchain",
    description="transferchain abci read client",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/transferchain/tcabci-read-python-client",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
