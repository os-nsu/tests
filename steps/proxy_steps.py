# steps/proxy_steps.py

import os
import subprocess
import time
import pytest

from steps.build_steps import simple_clean, make


def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")
