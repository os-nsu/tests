# steps/proxy_steps.py

import os
import subprocess
import time
import pytest

from steps.build_steps import simple_clean, make


def run_proxy(project_dir, proxy_bin_name, args=[], timeout=None, env=None, wait_until_end=True):
    """
    Runs the proxy with specified arguments.

    If wait is True, waits for the process to complete and returns the CompletedProcess object.
    If wait is False, starts the process and returns the Popen object.
    """
    try:
        if wait_until_end:
            result = subprocess.run([proxy_bin_name] + args, cwd=project_dir, check=False, capture_output=True, text=True, timeout=timeout, env=env)
            return result
        else:
            proc = subprocess.Popen([proxy_bin_name] + args, cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            return proc
    except subprocess.TimeoutExpired:
        pytest.fail(f"Proxy not finished in {timeout} seconds.")
    except Exception as e:
        pytest.fail(f"Can't start proxy with args {args}, {e}")

def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")

def build_and_run_proxy(project_dir, proxy_bin_name, log_file_path=None, proxy_timeout=0, args=[], make_args=[], extra_env={}, env=None, wait_until_end=True):
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
    make(project_dir, make_args, extra_env)

    if log_file_path and os.path.exists(log_file_path):
        os.remove(log_file_path)

    result = run_proxy(project_dir, proxy_bin_name, args=args, env=env, timeout=proxy_timeout if wait_until_end else None, wait_until_end=wait_until_end)

    return result
