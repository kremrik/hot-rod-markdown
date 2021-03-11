# python-template
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### How to use
1. Create a new GitHub repo using this as a template
1. Clone said repo
1. Change all references to "python-template":
    - in `.package-name`
    - the `python_template` directory name
1. Run `make set-hooks` to set the Makefile pipeline to run before each commit (you may want/need to remove some of the dependencies in the `check` recipe)
1. Install the development dependencies:
    - with pip (ensure you are in the proper environment): `pip install -r dev_dependencies.txt`
