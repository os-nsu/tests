# steps/build_steps.py

import os

from steps.utils import run_command

def simple_make(project_dir):
	return make(project_dir)

def simple_clean(project_dir):
	res = run_command(args=["make", "clean"], cwd=project_dir, check=True)
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

	return res
