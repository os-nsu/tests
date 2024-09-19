import os
import pytest

# CLI arguments parser
def pytest_addoption(parser):
	parser.addoption("--src", action="store")
	parser.addoption("--bin", action="store")

@pytest.fixture(scope="session")
def project_dir(request):
	proxy_src = request.config.getoption("--src")
	if proxy_src is None or len(proxy_src) == 0:
		pytest.fail("No source path was given. Use --src")
	return os.path.abspath(proxy_src)

@pytest.fixture(scope="session")
def proxy_bin_name(request, project_dir):
	proxy_bin = request.config.getoption("--bin")
	if proxy_bin is None or len(proxy_bin) == 0:
		pytest.fail("No proxy bin name was given. Use --bin")
	return os.path.abspath(f"{project_dir}/{proxy_bin}")

@pytest.fixture(autouse=True)
def run_around_tests():
	# Do something before test

	yield # Run test

	# Do something after test
