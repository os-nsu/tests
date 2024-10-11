import os
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

@pytest.fixture(scope="session")
def can_collect_coredumps():
    """Checks if coredumps can be collected based on system settings."""
    try:
        with open("/proc/sys/kernel/core_pattern", "r") as f:
            pattern = f.read().strip()
        if not pattern:
            warnings.warn("Empty /proc/sys/kernel/core_pattern. Core dump checking is disabled.")
            return False
    except Exception as e:
        warnings.warn(f"Failed to read /proc/sys/kernel/core_pattern: {e}. Core dump checking is disabled.")
        return False

    # Check if ulimit -c is greater than 0
    try:
        result = subprocess.run(["ulimit", "-c"], shell=True, capture_output=True, text=True, executable='/bin/bash')
        if result.returncode != 0:
            warnings.warn("Failed to get ulimit -c. Core dump checking is disabled.")
            return False
        core_size = int(result.stdout.strip())
        if core_size == 0:
            warnings.warn("Core dump size is set to 0. Core dump checking is disabled.")
            return False
    except Exception as e:
        warnings.warn(f"Failed to check core dump size: {e}. Core dump checking is disabled.")
        return False
    
@pytest.fixture(autouse=True)
def run_around_tests(proxy_bin_name, core_pattern):
	# Do something before test
	start_coredumps = get_coredump_files(proxy_bin_path=proxy_bin_name, coredump_dir=coredump_dir, core_pattern=core_pattern)
	yield # Run test
	segfault_detected, segfault_details = check_for_coredump_difference(proxy_bin_path=proxy_bin_name, start_coredumps=start_coredumps, coredump_dir=coredump_dir, core_pattern=core_pattern)
	if segfault_detected:
		pytest.fail(segfault_details)
	# Do something after test
