"""
Setup script for Convo Programming Language
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
try:
    with open('requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    pass

setup(
    name="convo-lang",
    version="0.0.1",
    author="DreadHeadHippy",
    author_email="155098676+DreadHeadHippy@users.noreply.github.com",
    description="A natural programming language with conversational syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DreadHeadHippy/Convo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "discord": ["discord.py>=2.0.0"],
        "dev": ["pytest>=8.0.0", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "convo=convo.__main__:main",
        ],
    },
    package_data={
        "convo": ["*.md"],
    },
    include_package_data=True,
    zip_safe=False,
)
