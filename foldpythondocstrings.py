import sublime
import sublime_plugin


def fold_comments(view):
    for region in view.find_by_selector('string.quoted.double.block, string.quoted.single.block'):
        lines = view.lines(region)
        if len(lines) > 1:
            region = sublime.Region(lines[0].begin(), lines[-1].end())
            text = view.substr(region).strip()
            if text.startswith("'''") or text.startswith('"""'):
                fold_region = sublime.Region(lines[0].end(), lines[-1].end() - 3)
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
