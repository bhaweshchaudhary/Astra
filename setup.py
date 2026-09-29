from setuptools import setup, find_packages

setup(
    name="astra",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "astra = astra.cli:main"
        ]
    },
    author="bhaweshchaudhary",
    description="Astra: A Powerful Network Scanner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bhaweshchaudhary/astra",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
