#!/usr/bin/env python3
"""
Setup script for jcsdks.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from __init__.py
version = ""
with open(Path(__file__).parent / "jcsdks" / "__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

# Read README.md for long description
with open(Path(__file__).parent / "README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jcsdks",
    version=version,
    description="JavaCard SDK Manager - Helps configure and validate JavaCard SDKs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ibaibing",
    author_email="ibaibing@outlook.com",
    url="https://github.com/ibaibing/jcsdks",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "sctool>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jcsdks = jcsdks.cli:main",
        ],
        "sctool.plugins": [
            "sdks = jcsdks.cli:register",
        ],
    },
    keywords="javacard, sdk, manager, configuration, validation",
    license="MIT",
    project_urls={
        "Source": "https://github.com/ibaibing/jcsdks",
        "Bug Reports": "https://github.com/ibaibing/jcsdks/issues",
        "Documentation": "https://github.com/ibaibing/jcsdks",
    },
)
