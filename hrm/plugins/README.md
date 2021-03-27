## Plugins

### Overview
Each plugin acts on the contents of a single Markdown file (as a generator/stream) and, optionally, any values passed as arguments from the command-line.
It's completely up to you whether you wish to eagerly evaluate the contents of the file (possibly giving you the ability to determine IF those contents have changed) or process it line-by-line by exhausting the generator and yielding back the (possibly) transformed line.
Each plugin is dynamically loaded by the CLI and given a prettified subcommand name derived from the class name.

### Requirements
There are only two things required to create a plugin:
1. inherit from the `hrm.plugins._base.HotRodMarkdown` class
1. implement a single method (`transform`)

Below is a walk-through of the `change_headings.py` plugin demonstrating these, and some additional/optional, features.

```python INJECT_CODE(change_headings.py)
from hrm.plugins._base import HotRodMarkdown

from typing import Generator, Union


class ChangeHeadings(HotRodMarkdown):
    """
    Takes `change` as a required input, which represents
    the change in the number of heading '#' you wish to
    apply to each heading. For example:

    hrm change-headings --change 1

    would add one '#' to each heading
    """

    __help__ = "Adds/removes heading level(s)"

    change: int

    def transform(
        self,
        md_contents: Generator[str, None, None],
        **kwargs,
    ) -> Union[str, Generator[str, None, None]]:
        change = kwargs["change"]

        for line in md_contents:
            if not line.startswith("#"):
                yield line

            else:
                current_level = line.count("#")
                new_level = current_level + change
                level = "#" * new_level
                stripped_line = line.replace("#", "")
                new_line = f"{level}{stripped_line}"

                yield new_line
```

### Walk-through

#### `from hrm.plugins._base import HotRodMarkdown` [required]
The required base class

#### `__doc__` [optional]
Any docstrings you write at the plugin's class-level will be incorporated into the CLI's subcommand `hrm [sub-cmd] -h` option.

#### `__help__` [optional]
You can create a `__help__` attribute for your plugin to provide the user with a short description of the subcommand when running `hrm -h`

#### `change: int` [optional]
If your plugin requires additional arguments from the command line, you can simply use class annotations with type hints.
Any args generated this way will be fed into the `transform` method via `**kwargs`.
This example will create a _required_ option `change` that will can be set with `--change` at the command-line.
If you wished to make it optional, simply use `foo: Optional[int]` instead.

#### `change = kwargs["change"]` [optional]
As noted above, this is how you can access any command line options

### External plugins directory
You can store your own plugins in their own directory anywhere you like. 
Just point `hrm` to their location using the environment variable `HRM_PLUGINS`.
Once your plugin is created and the env var is set, running `hrm -h` again will now display the new option.

### Type hints
While not required, type-hinting your plugin is a great sanity check.
`mypy` can be used at the command-line, and some IDEs (like PyCharm) will automatically flag incompatible hints.
