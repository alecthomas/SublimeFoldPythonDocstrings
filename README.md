# Sublime Text - Fold Python Docstrings

This plugin folds/unfolds Python docstrings.

It makes this:

![Before folding](http://f.cl.ly/items/240v1D0z3x1s2T1J3u41/Screen%20Shot%202013-04-16%20at%2010.59.59%20AM.png)

Look like this:

![After folding](http://f.cl.ly/items/3O1r3h3g141j0q1T140r/Screen%20Shot%202013-04-16%20at%2011.02.13%20AM.png)

### Installation

Using [Package Control](https://sublime.wbond.net/installation), install the *"Fold Python Docstrings"* package.

### Key bindings

There are two commands exposed: `fold_python_docstrings` and `unfold_python_docstrings`.

On OSX these are bound to ⌘⇧- and ⌘⇧=, respectively.

### Configuration

The following settings can be changed in `User/Preferences.sublime-settings`:

**fold_python_docstrings_onload**

Set to `false` to disable folding on initial load

**fold_python_docstrings_number_of_lines**

Set to this to an integer to fold the docstring to this number of lines

