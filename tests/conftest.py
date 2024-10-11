import os
import subprocess
import pytest
import warnings

from steps.test_steps import(
	get_coredump_files,
	check_for_coredump_difference,
	get_coredump_pattern
)
# CLI arguments parser
def pytest_addoption(parser):
	parser.addoption("--src", action="store")
	parser.addoption("--proxy_timeout", action="store", type=int, default=1, help="Global timeout for tests in seconds.")
	parser.addoption("--coredump-dir", action="store", default="/proc/sys/kernel/core_pattern", help="Directory where coredump files are stored.")

@pytest.fixture(scope="session")
def project_dir(request):
	proxy_src = request.config.getoption("--src")
	if proxy_src is None or len(proxy_src) == 0:
		pytest.fail("No source path was given. Use --src")
	return os.path.abspath(proxy_src)

@pytest.fixture(scope="session")
def proxy_bin_name(request, project_dir):
	return os.path.abspath(f"{project_dir}/install/proxy")

@pytest.fixture(scope="session")
def proxy_timeout(request):
	return request.config.getoption("--proxy_timeout")

@pytest.fixture(scope="session")
def coredump_dir(request):
	"""Provides the coredump directory path."""
	return os.path.abspath(request.config.getoption("--coredump-dir"))

@pytest.fixture(scope="session")
def core_pattern():
	"""Read  coredump pattern from coredump_pattern_file."""
	return get_coredump_pattern()


def pytest_configure(config):
	config.coredump_check_possible = False

def pytest_sessionstart(session):
	"""Hook before all tests."""
	config = session.config
	core_pattern = get_coredump_pattern()

	if not core_pattern:
		warnings.warn("core_pattern is empty. Coredump checking is not possible.")
		return

	try:
		ulimit_output = subprocess.check_output('ulimit -c', shell=True, text=True).strip()
		if ulimit_output.lower() == 'unlimited':
			core_size = float('inf')
		else:
			core_size = int(ulimit_output)
		if core_size == 0:
			warnings.warn("Size core-files = 0. Checking coredump impossible.", UserWarning)
			return
	except ValueError:
		warnings.warn(f"Can't parse 'ulimit -c': '{ulimit_output}'. Checking coredump impossible.", UserWarning)
		return
	except Exception as e:
		warnings.warn(f"Can't check coredump size: {e}. Checking coredump impossible.", UserWarning)
		return

	if core_pattern.startswith('|'):
		warnings.warn("Coredumps are handled by an external program. Coredump checking is not possible.")
		return

	if os.path.isabs(core_pattern):
		directory = os.path.dirname(core_pattern)
	else:
		directory = os.getcwd()

	if not os.path.isdir(directory):
		warnings.warn(f"Coredump directory does not exist: {directory}. Coredump checking is not possible.")
		return

	config.coredump_check_possible = True

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
	config = item.config
	proxy_bin_name = item.funcargs.get('proxy_bin_name')
	coredump_dir = item.funcargs.get('coredump_dir')
	core_pattern = item.funcargs.get('core_pattern')

	if not config.coredump_check_possible or not proxy_bin_name or not coredump_dir or not core_pattern:
		yield
		return

	start_coredumps = get_coredump_files(proxy_bin_name, coredump_dir, core_pattern)

	yield

	segfault_detected, segfault_details = check_for_coredump_difference(proxy_bin_name, start_coredumps, coredump_dir, core_pattern)
	if segfault_detected:
		item._segfault_details = segfault_details

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	"""Make report for test"""
	outcome = yield
	report = outcome.get_result()

	if report.when == "call" and hasattr(item, '_segfault_details'):
		report.outcome = 'failed'
		report.longrepr = f"{report.longrepr or ''}\n--- Proxy produced coredump(s) ---\n{item._segfault_details}"