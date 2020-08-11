import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gendersdb",
    version="0.0.1",
    author="Meghan Utter and Nisha Prabhakar",
    author_email="utter2@llnl.gov, nisha.p@berkeley.edu",
    description="Centralized Node Attribute Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LLNL/HPCCEA/tree/gendersteam/2020/Genders",
    packages=setuptools.find_packages(),
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)
