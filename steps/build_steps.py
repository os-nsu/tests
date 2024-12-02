# steps/build_steps.py

import subprocess
import os
import sys

def simple_make(project_dir):
	return make(project_dir)

def simple_clean(project_dir):
	res = subprocess.run(["make", "clean"], cwd=project_dir, capture_output=True, check=False)
	assert res.returncode == 0, "make clean finished with no-zero return code"
	assert len(res.stderr) == 0, f"make clean has stderr '{res.stderr}'"
	return res

def make(project_dir, make_args=[], extra_env={}):
	"""Builds the proxy with specified flags."""
	env = os.environ.copy()
	env.update(extra_env)

	env.setdefault("COPT", "")
	env.setdefault("CFLAGS", "")

	env["COPT"] = f"-Werror -Wall {env['COPT']}"
	env["CFLAGS"] = f"-Og -fno-omit-frame-pointer -ggdb3 {env['CFLAGS']}"
	env["CXXFLAGS"] = f"{env['CFLAGS']} {env['COPT']}"

	res = subprocess.run(["make"] + make_args, cwd=project_dir, env=env, check=False, capture_output=True)

	# Show all output in tests
	print(res.stdout.decode('utf-8'), file=sys.stdout)
	print(res.stderr.decode('utf-8'), file=sys.stderr)

	assert res.returncode == 0, "make finished with no-zero return code"
	assert len(res.stderr) == 0, f"make output has stderr '{res.stderr}'"

	return res
