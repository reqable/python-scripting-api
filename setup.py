import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="reqable-scripting",
	version="1.1.0",
	author="MegatronKing",
	author_email="coding@reqable.com",
	url="https://reqable.com/docs/capture/addons",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.6"
)
