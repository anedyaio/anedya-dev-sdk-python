# setup.py

from setuptools import setup, find_packages

# Your package's long description, if you have one.
# You should replace 'README.md' with the actual name of your README file.

setup(
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['requests', 'time', 'json'],  # Add any required dependencies here
    include_package_data=True,
    # Add if you have non-Python files to include
)
