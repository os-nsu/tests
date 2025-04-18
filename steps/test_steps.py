# steps/test_steps.py

import os
import glob
import pytest
import warnings

from steps.utils import run_command


def check_file_exists(file_path):
	"""Check that a file exists."""
	return os.path.isfile(file_path)

def check_directory_exists(dir_path):
	"""Check that a directory exists."""
	return os.path.isdir(dir_path)

def get_coredump_pattern(coredump_path_file="/proc/sys/kernel/core_pattern"):
	"""Reads the coremudp_dir file."""
	if not check_file_exists(coredump_path_file):
		warnings.warn(f"Can't read {coredump_path_file}: file not exists")
		return None

	try:
		with open(coredump_path_file, "r") as f:
			pattern = f.read().strip()
		return pattern
	except Exception as e:
		pytest.fail(f"Can't read {coredump_path_file}: {e}")

def translate_core_pattern_to_path(proxy_bin_path, project_dir, core_pattern):
	if core_pattern.startswith('|'):
		return None, None

	if os.path.isabs(core_pattern):
		directory = os.path.dirname(core_pattern)
		pattern = os.path.basename(core_pattern)
	else:
		directory = project_dir
		pattern = core_pattern

	if not os.path.isdir(directory):
		pytest.fail(f"Coredump directory does not exist: {directory}")

	placeholder_mapping = {
		"%%": "%",
		"%e": os.path.basename(proxy_bin_path),
		"%E": os.path.basename(proxy_bin_path).replace('/', '!'),
		"%g": "*",
		"%h": "*",
		"%i": "*",
		"%I": "*",
		"%p": "*",
		"%P": "*",
		"%s": "*",
		"%t": "*",
		"%u": "*",
	}

	for placeholder, replacement in placeholder_mapping.items():
		pattern = pattern.replace(placeholder, replacement)

	return directory, pattern

def get_coredump_files(proxy_bin_path, project_dir, core_pattern):
	"""Returns a set of coredump files in the specified directory based on core_pattern."""
	directory, pattern = translate_core_pattern_to_path(proxy_bin_path, project_dir, core_pattern)
	if directory is None or pattern is None:
		# Проверка coredump невозможна
		return None
	full_pattern = os.path.join(directory, pattern)
	return set(glob.glob(full_pattern))

def check_for_coredump_difference(proxy_bin_path, project_dir, start_coredumps, core_pattern):
	"""Checks for new coredumps and returns True and details if a new coredump is found."""
	end_coredumps = get_coredump_files(proxy_bin_path, project_dir, core_pattern)
	if end_coredumps is None:
		return False, ""
	new_coredumps = end_coredumps - start_coredumps
	if new_coredumps:
		coredump_file = new_coredumps.pop()

		gdb_command = ["gdb", "--batch", "-ex", "bt", proxy_bin_path, coredump_file]
		gdb_result = run_command(gdb_command, cwd=project_dir, check=False)
		if gdb_result.stdout:
			segfault_details = f"Stacktrace from coredump ({coredump_file}):\n{gdb_result.stdout}"
		else:
			segfault_details = f"Failed to retrieve stacktrace from coredump ({coredump_file})."

		return True, segfault_details
	return False, ""

