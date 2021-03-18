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

#### Standard functionality
Run `hrm -h` for a listing of available commands

#### Extended functionality
YOu can create your own plugins (see [this guide](hrm/plugins/README.md)) and point `hrm` to their location using the environment variable `HRM_PLUGINS`.
This path is expected to be a directory.
Once your plugin is created and the env var is set, running `hrm -h` again will now display the new option.

## Example
One of the things Markdown struggles with a little bit is codeblocks.
Yes, they're formatted nicely in GitHub (for example), but it's generally a manual process to put code there and very inconvenient to update and test it.
`hrm` supplies you with a command called `inject-code` that allows you annotate a codeblock like the example below:
````
```python INJECT_CODE(example.py)
```
````
The `INJECT_CODE([filepath])` annotation tells `hrm` to load the file referenced by the `filepath` and insert the contents as-is between the triple backticks of the codeblock.
This will be done recursively from your `pwd` when run like
```
hrm inject-code
```
or (optionally) from a given path:
```
hrm inject-code path/to/dir-or-file
```
You can see an example of this [here](hrm/plugins/README.md))
