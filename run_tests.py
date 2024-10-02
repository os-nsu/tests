#!/usr/bin/env python

# The main entrypoint for running tests

import sys
import importlib.util

pytest = None

def import_pytest_if_installed():
	global pytest
	pkg_name = "pytest"

	if (spec := importlib.util.find_spec(pkg_name)) is not None:
		module = importlib.util.module_from_spec(spec)
		sys.modules[pkg_name] = module
		spec.loader.exec_module(module)
		pytest = module
		return True

	print(f"{pkg_name} is not installed")
	return False

def run_pytest():
	args = [sys.argv[0]]

	# Add path to folder with tests
	args += ["tests"]

	# Print shorter python tracebacks
	args += ["--tb=short"]

	# Generate xml report
	args += ["--junit-xml=report.xml"]

	# Show extra test summary
	args += ["-rA"]

	# Show verbose info where possible
	args += ["-v"]

	# Add custom args after predefined ones so they could be redefined
	args += sys.argv[1:]

	returncode = pytest.main(args)
	return True if returncode == 0 else False

def main():
	if not import_pytest_if_installed():
		return False

	return run_pytest()

if __name__ == "__main__":
	ret_code = 0 if main() else 1
	sys.exit(ret_code)
