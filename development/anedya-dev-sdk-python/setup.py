# setup.py

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Your package's long description, if you have one.
# You should replace 'README.md' with the actual name of your README file.

setup(
    name='anedya-sdk',
    version='0.1.1',
    description='Anedya SDK for IoT devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Saransh Jaiswal',
    url='',
    author_email='saranshjaiswal09@gmail.com',
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7, <4",
    install_requires=['requests'],  # Add any required dependencies here
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        # Add more classifiers as needed
    ],
    include_package_data=True,
    # Add if you have non-Python files to include
)
