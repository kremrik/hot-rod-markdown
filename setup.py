import hrm

from setuptools import find_packages, setup


DESCRIPTION = ""
AUTHOR = "Kyle Emrick"
GITID = "kremrik"


def get_package_name() -> str:
    packagefile = ".package-name"
    package = open(packagefile, "rt")\
        .read()\
        .strip()\
        .replace("-", "_")
    return package


setup(
    name=get_package_name(),
    version=hrm.__version__,
    author=AUTHOR,
    url="https://github.com/{}/{}".format(GITID, get_package_name()),
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("docs")),
    include_package_data=True,
    scripts=["bin/hrm"]
)
