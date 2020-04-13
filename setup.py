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
    install_requires=[line.strip() for line in open("requirements.txt", "r") if line.strip()],
    entry_points={
        "console_scripts": [
            "pathtree2dot = pltools.pathtree:main",
            "java_methods = pltools.java_methods:main",
            "c_defined_functions = pltools.c_defined_functions:main"
        ]
    }
)