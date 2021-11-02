from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in zoom_cart/__init__.py
from zoom_cart import __version__ as version

setup(
	name="zoom_cart",
	version=version,
	description="E-Commerce",
	author="Tridz",
	author_email="info@tridz.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
