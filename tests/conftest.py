import os
import pytest

# CLI arguments parser
def pytest_addoption(parser):
	parser.addoption("--src", action="store")

@pytest.fixture(scope="session")
def project_dir(request):
	"""Provides the project directory path."""
	proxy_src = request.config.getoption("--src")
	if proxy_src is None or len(proxy_src) == 0:
		pytest.fail("No source path was given. Use --src")
	return os.path.abspath(proxy_src)

@pytest.fixture(scope="session")
def proxy_bin_name(request, project_dir):
	return os.path.abspath(f"{project_dir}/install/proxy")

@pytest.fixture(autouse=True)
def run_around_tests():
	# Do something before test
	yield # Run test
	# Do something after test
