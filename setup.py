from setuptools import setup, find_packages
from codecs import open
from os import path

import os

here = path.abspath(path.dirname(__file__))

here = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(here, 'requirements.txt')
with open(requirements_path, 'r', encoding='utf-8') as f:
    install_requires = f.readlines()

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dream-my-plots",
    version="1.0.0",
    description="Create plots in Python with AI LLMs through langchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafah/dream-my-plots",
    author="MLJAR",
    author_email="mustafah.elbanna@gmail.com",
    license="Apache 2.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=open("requirements.txt").readlines(),
    include_package_data=True,
    python_requires='>=3.7.1',
    classifiers=[
    ],
    keywords=[
        "plot",
        "visualization",
        "charts",
        "matplotlib",
        "llm",
        "openai"
    ],
)
