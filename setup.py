import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysats",
    version="0.0.1",
    author="Fabio Isler",
    author_email="islerfab@gmail.com",
    description="Python bridge to use SATS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spectrumauctions/pysats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
