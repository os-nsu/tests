#!/usr/bin/env python

# run_tests.py

# The main entrypoint for running tests

import argparse
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

def run_tests(tags=None, full_logs=False, extra_args=None):
	"""
	Runs pytest with optional markers (tags) and optional "full logs" mode.
	"""
	if extra_args is None:
		extra_args = []

	pytest_cmd = [
		"tests",            # path to the tests folder
		"--tb=short",       # short tracebacks
		"-v",               # verbose (test names)
		"--order-dependencies",  # keep test order in dependencies(maybe do nothing)
	]

	if tags:
		# if user says --tags lab1 => tags=["lab1"]
		# or multiple --tags lab1 lab2 => tags=["lab1","lab2"]
		if "globaltest" not in tags:
			tags.append("globaltest")

		marker_expr = " or ".join(tags)
		pytest_cmd.extend(["-m", marker_expr])

	if full_logs:
		pytest_cmd.append("-rA") #if full_logs - write logs in all test, not only in failed

	pytest_cmd.extend(extra_args)

	print(f"[run_tests] Running pytest with: {pytest_cmd}")
	return pytest.main(pytest_cmd)

def main():
	if not import_pytest_if_installed():
		sys.exit(1)

	parser = argparse.ArgumentParser()
	parser.add_argument("--src", help="Path to the proxy source directory (passed to pytest).")
	parser.add_argument("--proxy_timeout", "-t", default="1", help="Proxy timeout (passed to pytest).")
	parser.add_argument("--labs", "-l", nargs="*", help="Markers to run (e.g. lab1, lab2, globaltest).")
	parser.add_argument("--full-logs", "-full", action="store_true", help="Show full logs for successful tests as well.")
	args, unknown = parser.parse_known_args()

	if args.src:
		unknown.append(f"--src={args.src}")
	if args.proxy_timeout:
		unknown.append(f"--proxy_timeout={args.proxy_timeout}")

	tags = args.labs or []

	success = run_tests(
		tags=tags,
		full_logs=args.full_logs,
		extra_args=unknown
	)

	sys.exit(0 if success == 0 else 1)

if __name__ == "__main__":
	main()
