from setuptools import setup, find_packages
from version.version import VERSION
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
CRIXS_VERSION = VERSION

setup(
    name="CRIXS",
    version=CRIXS_VERSION,
    packages=find_packages(),
    entry_points={},
    install_requires=["matplotlib>=3.4", "numpy>=1.15", "scipy>=1.7"],
    url="https://github.com/Coolphy/CRIXS",
    license="GNU General Public License v3.0",
    author="Yuan Wei",
    author_email="weiyuan.phy@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
