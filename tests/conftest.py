import os
import pytest

from steps.test_steps import(
	get_coredump_files,
	check_for_coredump_difference
)
# CLI arguments parser
def pytest_addoption(parser):
	parser.addoption("--src", action="store")
	parser.addoption("--proxy_timeout", action="store", type=int, default=1, help="Global timeout for tests in seconds.")
	parser.addoption("--coredump-dir", action="store", default="/var/lib/systemd/coredump", help="Directory where coredump files are stored.")

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

@pytest.fixture(autouse=True)
def run_around_tests(proxy_bin_name, coredump_dir):
	# Do something before test
	start_coredumps = get_coredump_files()
	yield # Run test
	check_for_coredump_difference(proxy_bin_name, start_coredumps, coredump_dir)
	# Do something after test
