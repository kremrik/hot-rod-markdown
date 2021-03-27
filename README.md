![](images/hot-rod-markdown.png)

# hot-rod-markdown
[![Python package](https://github.com/kremrik/hot-rod-markdown/actions/workflows/python-package.yml/badge.svg)](https://github.com/kremrik/hot-rod-markdown/actions/workflows/python-package.yml)
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Soup-up your Markdown!

## Installation
```
python -m pip install git+https://github.com/kremrik/hot-rod-markdown.git
```

## Motivation
Markdown is an incredible tool for technical writers.
It's easy to understand, always human-readable, and has the internet-equivalent [lifespan](https://brandur.org/fragments/graceful-degradation-time) of styrofoam.
For these reasons (and many more), it's a fantastic medium for communication.
`hrm` exists to make Markdown even more usable.

## Concepts
At its core, `hrm` is a command-line tool that walks a directory and applies a transformation to any Markdown files it encounters along the way.
These transformations may be accessed in two different ways:
1. The commands that are bundled with the `hrm` package:
    ```
    $ hrm -h
    usage: hrm [-h] {change-headings,inject-code} ...

    positional arguments:
    {change-headings,inject-code}
        change-headings     Adds/removes heading level(s)
        inject-code         Injects files into annotated codeblocks

    optional arguments:
    -h, --help            show this help message and exit
    ```
1. External plugins that you can create yourself (documentation [here](hrm/plugins/README.md))
Plugins provide a simple, easy way of essentially creating your own "DSL's" for Markdown.

## Example
Let's look at one example of a command `hrm` exposes by default.
Suppose you have a nice README.md where you wish to show a code snippet for your users:

````
# Title

## Example of a simple function
```python
def greet(name):
    return f"Hello, {name}'
```
````

Great!
Your users have an example of how to write a quick function in Python.
Wouldn't it suck though if, in your haste to write that example, you accidentally used different quotes in the return?
Unfortunately, the only way you'd know that is if you tested it, which means copying and pasting it into your REPL, or into a file to manually execute.
Now imagine having dozens of examples like this.
`hrm` offers you a simple framework for this very problem.
Take a look at the new example below:

````
# Title

## Example of a simple function
```python INJECT_CODE(example_greet.py)
```
````

Notice how we've included the `INJECT_CODE(example_greet.py)` annotation with the codeblock.
If we add the file `example_greet.py` to the same directory that the readme is located:
```python
def greet(name):
    return f"Hello, {name}"
```

and then in the same directory run

```
hrm inject-code
```

`hrm` will search the Markdown file for any `INJECT_CODE` annotations and insert the code from the corresponding file directly into the codeblock, yielding:

````
# Title

## Example of a simple function
```python INJECT_CODE(example_greet.py)
def greet(name):
    return f"Hello, {name}"
```
````

Now, you're free to test that example file like any other Python code.


