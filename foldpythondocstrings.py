import sublime
import sublime_plugin


def fold_comments(view):
    # Selector moved out for readability
    selectors = 'string.quoted.double.block, string.quoted.single.block'
    number_lines_to_fold = view.settings().get(
        "fold_python_docstrings_number_of_lines", 1
    )

    for region in view.find_by_selector(selectors):
        lines = view.lines(region)
        if len(lines) <= 1:
            continue

        region = sublime.Region(lines[0].begin(), lines[-1].end())
        text = view.substr(region).strip()
        if not text.startswith(("'''", '"""')):
            continue

        # Moved out for readability
        a = lines[number_lines_to_fold - 1].end()
        b = lines[-1].end() - 3

        fold_region = sublime.Region(a, b)
        view.fold(fold_region)


class FoldFilePythonDocstrings(sublime_plugin.EventListener):
    def on_load(self, view):
        if view.settings().get("fold_python_docstrings_onload", True):
            fold_comments(view)


class FoldPythonDocstringsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fold_comments(self.view)


class UnfoldPythonDocstringsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.unfold(self.view.find_by_selector('string'))
