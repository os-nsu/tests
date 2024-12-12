# steps/proxy_steps.py

import os
import subprocess
import time
import pytest

from steps.build_steps import simple_clean, make
from steps.utils import run_command, start_command


<<<<<<< HEAD
=======
def run_proxy(project_dir, proxy_bin_name, args=[], timeout=None, env=None, wait_until_end=True):
    """
    Runs the proxy with specified arguments.

    If wait is True, waits for the process to complete and returns the CompletedProcess object.
    If wait is False, starts the process and returns the Popen object.
    """
    try:
        cmd = [proxy_bin_name] + args
        if wait_until_end:
            result = run_command(cmd, cwd=project_dir, env=env, timeout=timeout, check=False)
            return result
        else:
            proc = start_command(cmd, cwd=project_dir, env=env, text=True)
            return proc
    except subprocess.TimeoutExpired:
        pytest.fail(f"Proxy not finished in {timeout} seconds.")
    except Exception as e:
        pytest.fail(f"Can't start proxy with args {args}, {e}")

>>>>>>> e73a8f0 (Add wrapper for subprocces.run and Popen, first version)
def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")
