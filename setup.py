#!/usr/bin/env python3
"""
Setup script for ParGaMD GUI
A web-based interface for configuring ParGaMD simulations
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pargamd-gui",
    version="1.3.0",
    author="ParGaMD GUI Contributors",
    author_email="contact@example.com",
    description="A web-based GUI for configuring ParGaMD simulations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ParGaMD-GUI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "pargamd-gui=ui_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/*", "*.html", "*.js", "*.css"],
    },
    keywords="molecular dynamics, simulation, GUI, ParGaMD, WESTPA, AMBER",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ParGaMD-GUI/issues",
        "Source": "https://github.com/yourusername/ParGaMD-GUI",
        "Documentation": "https://github.com/yourusername/ParGaMD-GUI#readme",
    },
)
