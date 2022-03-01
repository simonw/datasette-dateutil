from setuptools import setup
import os

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-dateutil",
    description="dateutil functions for Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-dateutil",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-dateutil/issues",
        "CI": "https://github.com/simonw/datasette-dateutil/actions",
        "Changelog": "https://github.com/simonw/datasette-dateutil/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_dateutil"],
    entry_points={"datasette": ["dateutil = datasette_dateutil"]},
    install_requires=["datasette", "python-dateutil"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx"]},
    tests_require=["datasette-dateutil[test]"],
)
