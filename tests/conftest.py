# tests/conftest.py

import os
import subprocess
import pytest
import warnings

from entities.proxy import Proxy
from steps.backup_utils import FileBackup
from steps.test_steps import(
	get_coredump_files,
	check_for_coredump_difference,
	get_coredump_pattern
)

# CLI arguments parser
def pytest_addoption(parser):
	parser.addoption("--src", action="store", help="Path to the proxy source directory.")
	parser.addoption("--lab", action="store", type=int, default=1, help = "Flag to the test system, in what lab start testing")
	parser.addoption("--proxy_timeout", action="store", type=int, default=1, help="Global timeout for tests in seconds.")

@pytest.fixture
def set_cwd_to_test_file_dir(request, monkeypatch):
    """
    Temporarily sets the working directory to the directory of the test file.
    Useful for tests that use relative paths to files.
    """
    test_dir = request.fspath.dirname
    monkeypatch.chdir(test_dir)

@pytest.fixture
def file_backup():
    fb = FileBackup()
    yield fb
    fb.restore_all()

@pytest.fixture(scope="session")
def lab_number(request):
	lab_number = request.config.getoption("--lab")
	if lab_number not in [1,2,3,4]:
		pytest.fail("No lab_num was given. Use --lab")
	return lab_number

@pytest.fixture(scope="session")
def proxy_dir(request):
	proxy_src = request.config.getoption("--src")
	if proxy_src is None or len(proxy_src) == 0:
		pytest.fail("No source path was given. Use --src")
	return os.path.abspath(proxy_src)

@pytest.fixture(scope="session")
def proxy_bin_dir(proxy_dir):
	return os.path.join(proxy_dir, "install")

@pytest.fixture(scope="session")
def proxy_bin(proxy_bin_dir):
    return os.path.join(proxy_bin_dir, "proxy")

@pytest.fixture(scope="session")
def proxy_bin(proxy_bin_dir):
    return os.path.join(proxy_bin_dir, "proxy")

@pytest.fixture(scope="session")
def proxy_logger_lib(proxy_bin_dir):
    return os.path.join(proxy_bin_dir, "liblogger.so")

@pytest.fixture(scope="session")
def proxy_bin_plugins_dir(proxy_bin_dir):
	return os.path.join(proxy_bin_dir, "plugins")

@pytest.fixture(scope="session")
def proxy_plugins_greeting_bin(proxy_bin_plugins_dir):
	return os.path.join(proxy_bin_plugins_dir, "greeting.so")

@pytest.fixture
def current_dir(request):
    return os.path.dirname(request.fspath)

@pytest.fixture(scope="session")
def proxy_timeout(request):
	return request.config.getoption("--proxy_timeout")

@pytest.fixture(scope="session")
def core_pattern():
	"""Read  coredump pattern from coredump_pattern_file."""
	return get_coredump_pattern()

def pytest_configure(config):
	config.coredump_check_possible = False
	config.core_pattern = ""

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
	config.core_pattern = core_pattern

	warnings.warn(f"Coredump checking is turned on, core_pattern: {core_pattern}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
	config = item.config
	proxy_bin_name = item.funcargs.get('proxy_bin_name')
	proxy_dir = item.funcargs.get('proxy_dir')
	core_pattern =config.core_pattern

	if not config.coredump_check_possible or not proxy_bin_name or not core_pattern or not proxy_dir:
		yield
		return

	start_coredumps = get_coredump_files(proxy_bin_name, proxy_dir, core_pattern)

	yield

	segfault_detected, segfault_details = check_for_coredump_difference(proxy_bin_name, proxy_dir, start_coredumps, core_pattern)
	if segfault_detected:
		item._segfault_details = segfault_details

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	"""Make report for test"""
	outcome = yield
	report = outcome.get_result()

	allow_coredump = item.get_closest_marker('allow_coredump')

	if report.when == "call" and hasattr(item, '_segfault_details'):
		# If allow_coredump mark is set then we don't modify test outcome
		if not allow_coredump:
			report.outcome = 'failed'

		if report.longrepr:
			report.longrepr.addsection("Proxy produced coredump(s)", item._segfault_details)
		else:
			report.longrepr = f"--- Proxy produced coredump(s) ---\n{item._segfault_details}"

@pytest.fixture
def proxy_fixture(proxy_dir, proxy_bin_name, proxy_timeout):
	proxy = Proxy(project_dir=proxy_dir,
				  proxy_bin_name=proxy_bin_name,
				  proxy_timeout=proxy_timeout
				)
	return proxy
