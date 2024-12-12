# steps/build_steps.py

import os

from steps.utils import run_command

def simple_make(project_dir):
	return make(project_dir)

def simple_clean(project_dir):
	res = run_command(["make", "clean"], cwd=project_dir)
	assert res.returncode == 0, "make clean finished with no-zero return code"
	assert len(res.stderr) == 0, f"make clean has stderr '{res.stderr}'"
	return res

def make(project_dir, make_args=[], extra_env={}, check=True):
	"""Builds the proxy with specified flags."""
	env = os.environ.copy()
	env.update(extra_env)

	env.setdefault("COPT", "")
	env.setdefault("CFLAGS", "")

	env["COPT"] = f"-Werror -Wall {env['COPT']}"
	env["CFLAGS"] = f"-Og -fno-omit-frame-pointer -ggdb3 {env['CFLAGS']}"
	env["CXXFLAGS"] = f"{env['CFLAGS']} {env['COPT']}"

	res = run_command(["make"] + make_args, cwd=project_dir, env=env, check=check)

	if check:
		assert len(res.stderr) == 0, f"make output has stderr '{res.stderr}'"

	return res
