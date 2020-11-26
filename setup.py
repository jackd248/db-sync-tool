import setuptools
from db_sync_tool import info

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="db_sync_tool-kmi",
    version=info.__version__,
    author="Konrad Michalik",
    author_email="support@konradmichalik.eu",
    description="Synchronize a database from and to client systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=info.__homepage__,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
