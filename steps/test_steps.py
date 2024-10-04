#steps/test_steps.py

import os
import subprocess
import glob
import pytest

def get_coredump_files(coredump_dir="/proc/sys/kernel/core_pattern"):
	"""Returns a set of coredump files in the specified directory."""
	return set(glob.glob(os.path.join(coredump_dir, 'core.*')))

def check_for_coredump_difference(proxy_bin_name, start_coredumps, coredump_dir):
	"""Checks for new coredumps and prints a stack trace if found."""
	end_coredumps = get_coredump_files(coredump_dir)
	new_coredumps = end_coredumps - start_coredumps
	if new_coredumps:
		coredump_file = new_coredumps.pop()

		gdb_command = f"gdb --batch -ex 'bt' {proxy_bin_name} {coredump_file}"
		gdb_result = subprocess.run(gdb_command, capture_output=True, text=True, shell=True)
		if gdb_result.stdout:
			print("Stacktrace from coredump:\n")
			print(gdb_result.stdout)
		else:
			print("Failed to retrieve stacktrace from coredump.")

		pytest.fail("Proxy crashed and produced a coredump.")
