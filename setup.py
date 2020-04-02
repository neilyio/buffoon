import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="buffoon",
    version="0.0.1",
    author="Neil Hansen",
    author_email="neil.hansen.31@gmail.com",
    description="Send Python logs directly to an Emacs buffer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neilyio/buffoon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
