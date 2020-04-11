import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pltools-mr6r4y", # Replace with your own username
    version="0.1.0",
    author="mr6r4y",
    author_email="mr6r4y@example.com",
    description="Tools for source audit vizualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr6r4y/pltools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Quality Assurance"
    ],
    python_requires='>=3.6',
    install_requires=[
        "antlr4-python3-runtime==4.8",
        "graphviz>=0.13.2",
        "pycairo>=1.19.1",
        "ruamel.yaml>=0.16.10",
        "ruamel.yaml.clib>=0.2.0",
        "vext>=0.7.3",
        "vext.gi>=0.7.0",
        "xdot>=1.1",
    ],
    entry_points={
        "console_scripts": [
            "pathtree2dot = pltools.pathtree:main",
        ]
    }
)