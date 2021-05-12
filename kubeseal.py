import re
import subprocess

import sublime
import sublime_plugin

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

settings = None

def plugin_loaded():
	'''
	Called when the plugin is loaded, used to load the settings for the package.
	'''
	global settings
	settings = sublime.load_settings('kuebseal.sublime-settings')

class ConvertSecret(object):
	'''
	Wrapper for the process used to convert a Secret to a SealedSecret using kubeseal.

	:param sublime.View view: The view of the file to be converted.
	'''
	def __init__(self, view):
		self.view = view
		self.window = view.window()
		self.encoding = view.encoding()

		if self.encoding == 'Undefined':
			self.encoding = 'utf-8'

		self.cmd = settings.get('cmd', ['kubeseal', '-o', 'yaml']) # < current view > replaced current view

	def convert(self, region):
		'''
		Attempts to convert the contents of the current view from a Secret manifest to a SealedSecret manifest.

		:param sublime.Region region: The region for the file to convert
		:returns: str: Returns the SealedSecret manifest if no errors arose, else the original content.
		'''
		contents = self.view.substr(region)

		# run the kubeseal command
		output, error = self._exec(contents)
		if error:
			# there was an error, display it
			self._show_errors(error)

			# return the original content
			return contents

		# hide any existing errors
		self._hide_errors()

		# return the converted output
		return output

	def _exec(self, stdin):
		'''
		Runs kubeseal with the given input.

		:param str stdin: Stdin for the process, the file content to convert
		:returns: stdout, stderr: Returns the SealedSecret manifest if successful, an empty stdout
			and error if unsuccessful.
		'''
		proc = subprocess.Popen(
			self.cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)

		stdout, stderr = proc.communicate(stdin.encode())
		if stderr or proc.returncode != 0:
			return '', stderr.decode('utf-8')
		return stdout.decode(self.encoding), None

	def _show_errors(self, errors):
		'''
		Show the stderr of a failed process in an output panel.

		:param str stderr: Stderr output of a process.
		'''
		panel = self.window.create_output_panel('kubeseal')
		panel.set_scratch(True)
		panel.run_command('select_all')
		panel.run_command('right_delete')
		panel.run_command('insert', {'characters': ANSI_ESCAPE.sub('', errors)})
		self.window.run_command('show_panel', {'panel': 'output.kubeseal'})

	def _hide_errors(self):
		'''
		Hide any previously displayed error panel.
		'''
		self.window.run_command('hide_panel', {'panel': 'output.kubeseal'})

class KubesealCommand(sublime_plugin.TextCommand):
	'''
	The `kubeseal` command, invoked by the command palette.
	'''
	def run(self, edit):
		'''
		Converts the current file viewed, replacing its contents.
		'''
		converter = ConvertSecret(self.view)

		# get the entire view region
		region = sublime.Region(0, self.view.size())

		# run the formatter with the given region
		replacement = converter.convert(region)

		# replace the region if the content has changes
		if self.view.substr(region) != replacement:
			self.view.replace(edit, region, replacement)
