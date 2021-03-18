## Plugins

### Overview
Each plugin acts on the contents of a single Markdown file (as a generator/stream) and nothing more.
The plugin is dynamically loaded by the CLI, which uses a prettified module name as the subcommand.

### Requirements
There are three things required to create a plugin:
1. inherit from the `_base.HotRodMarkdown` class
1. name the class `Command`
1. implement a single method (`transform`)

That's it. 
See below for a short and sweet example of the `change_headings.py` plugin demonstrating some additional features.

```python INJECT_CODE(change_headings.py)
from hrm.plugins._base import HotRodMarkdown

from typing import Generator, Union


class Command(HotRodMarkdown):
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

### Optionally...
There are several things you'll notice about the above example that aren't strictly required:

#### Help
You can create a `__help__` attribute for your plugin to provide the user with a short description of the subcommand when running `hrm -h` 

#### Documentation/description
Any docstrings you write at the plugin's class-level will be incorporated into the CLI's subcommand `hrm [sub-cmd] -h` option.


#### Additional CLI arguments
If your plugin requires additional arguments from the command line, you can simply use class annotations with type hints (ie, `foo: Optional[int]` for an option argument).
Any args generated this way will be fed into the `transform` method via `**kwargs`.

#### Type hints
While not required, type-hinting your plugin is a great sanity check.
`mypy` can be used at the command-line, and some IDEs (like PyCharm) will automatically flag incompatible hints.
