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

### Optionally...

##### Help
Optionally, and quite nicely, you can create a `__help__` attribute for your plugin to provide the user with helpful information via the CLI.

##### Documentation/description
Additionally, any docstrings you write at the plugin's class-level will be incorporated into the CLI's subommand `-h/--help` option.


##### Additional CLI arguments
