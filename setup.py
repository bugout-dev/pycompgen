from setuptools import find_packages, setup

with open("pycompgen/version.txt") as ifp:
    VERSION = ifp.read().strip()

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="pycompgen",
    version=VERSION,
    packages=find_packages(),
    package_data={"pycompgen": ["py.typed"]},
    install_requires=[],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
        ],
        "distribute": [
            "setuptools",
            "twine",
            "wheel",
        ],
    },
    description="pycompgen: Generate shell completions for Python CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Moonstream",
    author_email="engineering@moonstream.to",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    url="https://github.com/bugout-dev/pycompgen",
    entry_points={"console_scripts": []},
    include_package_data=True,
)
