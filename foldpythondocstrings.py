import sublime
import sublime_plugin


def fold_comments(view):
    for region in view.find_by_selector('string'):
        lines = view.lines(region)
        if len(lines) > 1:
            region = sublime.Region(lines[0].begin(), lines[-1].end())
            text = view.substr(region).strip()
            if text.startswith("'''") or text.startswith('"""'):
                fold_region = sublime.Region(lines[0].end() - 1, lines[-1].end() - 3)
                view.fold(fold_region)


class FoldFilePythonDocstrings(sublime_plugin.EventListener):
    def on_load(self, view):
        fold_comments(view)


class FoldPythonDocstringsCommand(sublime_plugin.TextCommand):
    """This is a docstring.

    moo bar
    """
    def run(self, edit):
        fold_comments(self.view)
