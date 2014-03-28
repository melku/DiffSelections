import sublime
import sublime_plugin

from os import path
import itertools
import subprocess
import tempfile

# This plugin takes the two first selections in the current view and calls diff tool with these two
# selections as arguments.
#
# Example call:
# >>> view.run_command('diff_selections', {'difftool':'p4merge'})

class DiffSelectionsCommand(sublime_plugin.TextCommand):

    def run(self, edit, difftool):

        view = self.view

        # Diff tools require files. Create a temporary directory to put the temporary files.
        with tempfile.TemporaryDirectory() as tmpdir:

            leftfile = path.join(tmpdir, 'left')
            rightfile = path.join(tmpdir, 'right')

            selections = [view.substr(s) for s in itertools.islice(view.sel(), 2)]

            with open(leftfile, 'w') as left:
                left.write(selections[0])

            with open(rightfile, 'w') as right:
                right.write(selections[1])

            # Use check_call to wait for the diff tool to quit, in order to keep the temporary files.
            subprocess.check_call([difftool, leftfile, rightfile])
