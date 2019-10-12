import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["pandas"]

setuptools.setup(
        name="pandas_prices",
        version="0.0.1",
        author="Dmitri Kourbatsky",
        author_email="camel109@gmail.com",
        decription="calculate and allow for queries exchange rates database",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dimonf/pandas_prices.git",
#        packages = setuptools.find_packages(),
        packages = ['pandas_prices'],
        package_dir={'pandas_prices':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=requirements,
)

