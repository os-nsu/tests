import subprocess
import time
import os
import pytest
import subprocess
from steps.build_steps import simple_clean, make

class Proxy:
	def __init__(self, project_dir=None, proxy_bin_name=None, config_path=None, proxy_timeout=0):
		self._project_dir = project_dir
		self._proxy_bin_name = proxy_bin_name
		self._config_path = config_path
		self._proxy_timeout = proxy_timeout
		self._last_modified_time = self._get_last_modified_time()

		if config_path and not os.path.exists(config_path):
			self._create_default_config(config_path)
		self._config_content = self._read_config() if config_path else ""

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
		self.config_content = new_content
		self.last_modified_time = self._get_last_modified_time()

	def get_config_content(self):
		return self.config_content

	def run_proxy(self,args=[], timeout=None, env=None, wait_until_end=True):
		"""
		Runs the proxy with specified arguments.

		If wait is True, waits for the process to complete and returns the CompletedProcess object.
		If wait is False, starts the process and returns the Popen object.
		"""
		try:
			if wait_until_end:
				result = subprocess.run([self.proxy_bin_name] + args, cwd=self.project_dir, check=False, capture_output=True, text=True, timeout=timeout, env=env)
				return result
			else:
				proc = subprocess.Popen([self.proxy_bin_name] + args, cwd=self.project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
				return proc
		except subprocess.TimeoutExpired:
			pytest.fail(f"Proxy not finished in {timeout} seconds.")
		except Exception as e:
			pytest.fail(f"Can't start proxy with args {args}, {e}")

	def build_and_run_proxy(self, log_file_path=None, args=[], make_args=[], extra_env={}, make_env=None, wait_until_end=True):
		"""
		Builds the proxy and runs it with specified arguments.

		Parameters:
			args: Arguments to pass to run proxy .
			make_args: Arguments to pass to make proxy.
			extra_env: Extra environment variables to make proxy.
			env: Environment variables to run proxy.
			wait_until_end: If True, waits for the proxy to finish.

		Returns:
			If wait_until_end=True, returns the CompletedProcess object.
			If wait_until_end=False, returns the Popen object.
		"""
		simple_clean(self.project_dir)
		make(self.project_dir, make_args, extra_env)

		if log_file_path and os.path.exists(log_file_path):
			os.remove(log_file_path)

		result = self.run_proxy(args=args, env=make_env, timeout=self.proxy_timeout if wait_until_end else None, wait_until_end=wait_until_end)

		return result