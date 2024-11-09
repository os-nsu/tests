#steps/proxy_steps.py

import os
import subprocess
import time
import pytest

from steps.build_steps import simple_clean, simple_make


def start_proxy(project_dir, proxy_bin_name, args=[]):
	"""Starts the proxy process and returns the Popen object."""
	try:
		proc = subprocess.Popen([proxy_bin_name] + args, cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		return proc
	except Exception as e:
		pytest.fail(f"Can't start proxy: {e}")

def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")

def run_proxy_with_args(project_dir, proxy_bin_name, args, timeout=None):
	"""Runs the proxy with specified arguments and returns the CompletedProcess object."""
	try:
		result = subprocess.run([proxy_bin_name] + args, cwd=project_dir, check=False, capture_output=True, text=True, timeout=timeout)
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy not finished in {timeout} seconds.")
	except Exception as e:
		pytest.fail(f"Can't start proxy with args {args}: {e}")
	return result

def build_and_start_proxy(project_dir, proxy_bin_name, proxy_timeout, log_file_path):
    # Clean, build, clean log_file and start the proxy
    simple_clean(project_dir)
    simple_make(project_dir)

    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    proc = start_proxy(project_dir, proxy_bin_name)
    time.sleep(proxy_timeout)
    return proc

def build_and_start_and_run_proxy(project_dir, proxy_bin_name, proxy_timeout, args, log_file_path):
	proc = build_and_start_proxy(project_dir, proxy_bin_name, proxy_timeout, log_file_path)
	run_proxy_with_args(project_dir, proxy_bin_name, args, timeout=proxy_timeout)
	return proc
