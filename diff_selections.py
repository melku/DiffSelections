import sublime
import sublime_plugin

from os import path
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

        # We only want the two first selections, keep a counter
        i = 0

        # Diff tools require files. Create a temporary directory to put the temporary files.
        with tempfile.TemporaryDirectory() as tmpdir:

            leftfile = path.join(tmpdir, 'left')
            rightfile = path.join(tmpdir, 'right')

            for s in view.sel():
                if i == 0:
                    with open(leftfile, 'w') as left:
                        left.write(view.substr(s))
                if i == 1:
                    with open(rightfile, 'w') as right:
                        right.write(view.substr(s))
                i+=1

            # Use check_call to wait for the diff tool to quit, in order to keep the temporary files.
            subprocess.check_call([difftool, leftfile, rightfile])
