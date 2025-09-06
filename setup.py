"""
Setup script for Alayatales Temple Management System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="alayatales",
    version="1.0.0",
    author="Temple Heritage Team",
    author_email="support@alayatales.com",
    description="A comprehensive temple management system for preserving and sharing temple heritage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/alayatales",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Database :: Front-Ends",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alayatales=app:main",
        ],
    },
    keywords="temple management heritage culture streamlit mongodb",
    project_urls={
        "Bug Reports": "https://github.com/your-username/alayatales/issues",
        "Source": "https://github.com/your-username/alayatales",
        "Documentation": "https://github.com/your-username/alayatales#readme",
    },
)