from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xmatrix",
    version="1.4.2",
    author="Xanonymous",
    author_email="trusaidlin@gmail.com",
    description="Help you calculate matrix.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xanonymous-GitHub/xmatrix",
    packages=['xmatrix'],
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
