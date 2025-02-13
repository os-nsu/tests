import subprocess
import os
import pytest
import subprocess
from steps.build_steps import make_clean, make
from steps.utils import run_command, start_command

class Proxy:
	def __init__(self, project_dir=None, proxy_bin_name=None, proxy_timeout=0):
		self._project_dir = project_dir
		self._proxy_bin_name = proxy_bin_name
		self._log_file_path = os.path.join(project_dir, "logs/proxy.log") if project_dir else None
		self._proxy_timeout = proxy_timeout
		self._config_path = os.path.join(project_dir, "config.conf") if project_dir else None

		if self._config_path:
			self._create_default_config(self._config_path)
			self._config_content = self._read_config()
		if self._log_file_path:
			self._create_default_log_file(self._log_file_path)

		self._last_modified_time = self._get_last_modified_time()


	@property
	def project_dir(self):
		return self._project_dir

	@project_dir.setter
	def project_dir(self, value):
		if not isinstance(value, str) or not value:
			raise ValueError("project_dir must be a non-empty string")
		self._project_dir = value

	@property
	def proxy_bin_name(self):
		return self._proxy_bin_name

	@proxy_bin_name.setter
	def proxy_bin_name(self, value):
		if not isinstance(value, str) or not value:
			raise ValueError("proxy_bin_name must be a non-empty string")
		self._proxy_bin_name = value

	@property
	def config_path(self):
		return self._config_path

	@config_path.setter
	def config_path(self, value):
		if not isinstance(value, str) or not value:
			raise ValueError("config_path must be a non-empty string")
		self._config_path = value

	@property
	def log_file_path(self):
		return self._log_file_path

	@log_file_path.setter
	def log_file_path(self, value):
		if not isinstance(value, str) or not value:
			raise ValueError("log_file_path must be a non-empty string")
		self._log_file_path = value

	@property
	def proxy_timeout(self):
		return self._proxy_timeout

	@proxy_timeout.setter
	def proxy_timeout(self, value):
		if not isinstance(value, (int, float)) or value <= 0:
			raise ValueError("proxy_timeout must be a positive number")
		self._proxy_timeout = value

	@property
	def last_modified_time(self):
		return self._last_modified_time

	@last_modified_time.setter
	def last_modified_time(self, value):
		if not isinstance (value, (int, float)) or value <= 0:
			raise ValueError("last_modified_time must be a positive number")
		self._proxy_timeout = value

	def _create_default_config(self, config_path):
		with open(config_path, 'w') as file:
			file.write("")

	def _create_default_log_file(self, log_file_path):
		log_dir = os.path.dirname(log_file_path)
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		with open(log_file_path, 'w') as file:
			file.write("")

	def _read_config(self):
		with open(self.config_path, "r") as f:
			return f.read()

	def _get_last_modified_time(self):
		return os.path.getmtime(self.config_path) if self.config_path else None

	def has_config_changed(self):
		current_time = self._get_last_modified_time()
		if current_time != self.last_modified_time:
			self.last_modified_time = current_time
			return True
		return False

	def update_config(self, new_content):
		with open(self.config_path, "w") as f:
			f.write(new_content)

	def run_proxy(self, args=[], env=None, timeout=None, wait_until_end=True, check=True):
		"""
		Runs the proxy with specified arguments.

		If wait is True, waits for the process to complete and returns the CompletedProcess object.
		If wait is False, starts the process and returns the Popen object.
		"""
		cmd = [self.proxy_bin_name] + args
		if wait_until_end:
			result = run_command(cmd, cwd=self.project_dir, extra_env=env, timeout=timeout, check=check)
			return result
		else:
			proc = start_command(cmd, cwd=self.project_dir, env=env, text=True)
			return proc

	def build_and_run_proxy(self, proxy_args=[], proxy_env=None, make_args=[], make_env={}, wait_until_end=True, check=True):
		"""
		Builds the proxy and runs it with specified arguments.

		Parameters:
			proxy_args: Arguments to pass to run proxy .
   			proxy_env: Environment variables to run proxy.
			make_args: Arguments to pass to make proxy.
			make_env: Extra environment variables to make proxy.
			wait_until_end: If True, waits for the proxy to finish.
			check: If True, check for common errors

		Returns:
			If wait_until_end=True, returns the CompletedProcess object.
			If wait_until_end=False, returns the Popen object.
		"""
		make_clean(self.project_dir)
		make(self.project_dir, make_args, make_env, check=check)

		if self.log_file_path and os.path.exists(self.log_file_path):
			os.remove(self.log_file_path)

		result = self.run_proxy(args=proxy_args, env=proxy_env, timeout=self.proxy_timeout if wait_until_end else None, wait_until_end=wait_until_end, check = check)

		return result