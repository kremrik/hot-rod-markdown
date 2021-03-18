![](images/hot-rod-markdown.png)

# hot-rod-markdown
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Soup-up your Markdown!

## Motivation
Markdown is God's gift to technical writers.
It's easy to understand, always human-readable, and has the internet-equivalent [lifespan](https://brandur.org/fragments/graceful-degradation-time) of styrofoam.
For these reasons (and many more), it's a fantastic medium for communication.
`hrm` exists simply to make Markdown even more usable.
It does this by 
1. offering great quality-of-life functionality right out of the box
1. offering a simple (and easy) plugin model for rapid extensions

## Installation
```instructions```

## Usage
`hrm` is a command-line tool primarily, but as mentioned above it offers generic/standard functionality as well as extensible functionality

### Standard functionality
Run `hrm -h` for a listing of available commands

### Extended functionality
YOu can create your own plugins (see [this guide](hrm/plugins/README.md)) and point `hrm` to their location using the environment variable `HRM_PLUGINS`.
This path is expected to be a directory.
Once your plugin is created and the env var is set, running `hrm -h` again will now display the new option.
