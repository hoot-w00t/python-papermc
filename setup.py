import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open("requirements.txt", "r") as h:
        requirements = h.read().splitlines()

except:
    requirements = []

setuptools.setup(
    name="python-papermc",
    version="1.0.0",
    author="akrocynova",
    author_email="",
    description="Python wrapper for the PaperMC Downloads API (https://papermc.io)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoot-w00t/python-papermc",
    packages=["papermc"],
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=requirements,
    python_requires=">=3.5"
)