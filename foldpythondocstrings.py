import sublime
import sublime_plugin

docstring_selectors = [
    'string.quoted.double.block',
    'string.quoted.single.block',
    'string.quoted.docstring',
    'comment.block',
]

docstring_startswith = [
    "'''",
    '"""',
    'r"""',
]


def fold_comments(view):
    number_lines_to_fold = view.settings().get('fold_python_docstrings_number_of_lines', 1)
    for region in view.find_by_selector(', '.join(docstring_selectors)):
        lines = view.lines(region)
        if len(lines) <= 1:
            continue

        region = sublime.Region(lines[0].begin(), lines[-1].end())
        text = view.substr(region).strip()

        if not (text.startswith(tuple(docstring_startswith))):
            continue

        # Handle docstrings with just quotes on the first line.
        if text[3:4] in '\n\r':
            leading = len(text[4:]) - len(text[4:].lstrip())
            region = sublime.Region(lines[0].end(), lines[1].begin() + leading)
            view.fold(region)
            start = 1
        else:
            start = 0

        fold_region = sublime.Region(
            lines[start+number_lines_to_fold-1].end(), lines[-1].end() - 3)
        view.fold(fold_region)


class FoldFilePythonDocstrings(sublime_plugin.EventListener):

    def on_load(self, view):
        if view.settings().get('fold_python_docstrings_onload', True):
            fold_comments(view)


class FoldPythonDocstringsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        fold_comments(self.view)


class UnfoldPythonDocstringsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.unfold(self.view.find_by_selector('string'))
        self.view.unfold(self.view.find_by_selector('comment.block'))
