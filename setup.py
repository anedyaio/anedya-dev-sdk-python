# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Your package's long description, if you have one.
# You should replace 'README.md' with the actual name of your README file.

setup(
    name='anedya-dev-sdk',
    version='0.0.3a1',
    description='Anedya python based SDK for IoT devices. This SDK is currently under development. Future versions may include breaking changes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Anedya Systems',
    url='https://github.com/anedyaio/anedya-dev-sdk-pyhton',
    author_email='support@anedya.io',
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3",
    install_requires=['requests'],  # Add any required dependencies here
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        # Add more classifiers as needed
    ],
    include_package_data=True,
    # Add if you have non-Python files to include
)
