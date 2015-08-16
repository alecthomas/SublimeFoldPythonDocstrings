import sublime
import sublime_plugin

SELECTOR = 'string.quoted.double.block, string.quoted.single.block'


def fold_comments(view):
    # Settings
    number_lines_to_fold = view.settings().get(
        "fold_python_docstrings_number_of_lines", 1
    )
    show_ending_quotes_on_separate_line = view.settings().get(
        "fold_python_docstrings_show_ending_quotes_on_separate_line", False
    )

    for region in view.find_by_selector(SELECTOR):
        lines = view.lines(region)
        if len(lines) <= 1:
            continue

        region = sublime.Region(lines[0].begin(), lines[-1].end())
        text = view.substr(region).strip()
        if not text.startswith(("'''", '"""')):
            continue

        # **Edge Case**
        # If we have a comma, parenthesis or spaces after the quotes
        adjustment = 3
        while text[-1] != text[1]:
            adjustment += 1
            text = text[:-1]

        a = lines[number_lines_to_fold - 1].end()
        b = lines[-1].end() - adjustment

        # **Special Case**
        # When the doc-string ending quotes are on their own separate line,
        # show it on a separate line.
        if show_ending_quotes_on_separate_line:
            first_non_tab_or_space_char_at_end = text[:-3].rstrip(" \t")[-1]
            if first_non_tab_or_space_char_at_end == "\n":
                # Move to before the new-line.
                b -= len(text) - text.rfind("\n") - 3

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
        self.view.unfold(self.view.find_by_selector(SELECTOR))
