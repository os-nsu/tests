# steps/proxy_steps.py

import os
import pytest

from steps.build_steps import simple_clean, make
from steps.utils import run_command, start_command


<<<<<<< HEAD
<<<<<<< HEAD
=======
def run_proxy(project_dir, proxy_bin_name, args=[], timeout=None, env=None, wait_until_end=True):
=======
def run_proxy(project_dir, proxy_bin_name, args=[], timeout=None, env=None, wait_until_end=True, check=True):
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
    """
    Runs the proxy with specified arguments.

    If wait is True, waits for the process to complete and returns the CompletedProcess object.
    If wait is False, starts the process and returns the Popen object.
    """
    cmd = [proxy_bin_name] + args
    if wait_until_end:
        result = run_command(cmd, cwd=project_dir, env=env, timeout=timeout, check=check)
        return result
    else:
        proc = start_command(cmd, cwd=project_dir, env=env, text=True)
        return proc

>>>>>>> e73a8f0 (Add wrapper for subprocces.run and Popen, first version)
def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")
<<<<<<< HEAD
=======

def build_and_run_proxy(project_dir, proxy_bin_name, log_file_path=None, proxy_timeout=0, args=[], make_args=[], extra_env={}, env=None, wait_until_end=True, check=True):
    """
    Builds the proxy and runs it with specified arguments.

    Parameters:
        project_dir: Path to the project directory.
        proxy_bin_name: Name of the proxy binary.
        log_file_path: Path to the log file (optional).
        proxy_timeout: Time to wait after starting the proxy (make sense only if wait=True).
        args: Arguments to pass to run proxy .
        make_args: Arguments to pass to make proxy.
        extra_env: Extra environment variables to make proxy.
        env: Environment variables to run proxy.
        wait_until_end: If True, waits for the proxy to finish.

    Returns:
        If wait=True, returns the CompletedProcess object.
        If wait=False, returns the Popen object.
    """
    simple_clean(project_dir)
    make(project_dir, make_args, extra_env, check=check)

    if log_file_path and os.path.exists(log_file_path):
        os.remove(log_file_path)

    result = run_proxy(project_dir, proxy_bin_name, args=args, env=env, timeout=proxy_timeout if wait_until_end else None, wait_until_end=wait_until_end, check=check)

    return result
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
