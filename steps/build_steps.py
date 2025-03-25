# steps/build_steps.py

import os

from steps.utils import run_command

def make_clean(build_dir = None):
    """Cleans the project by calling make with the 'clean' target."""
    return make(build_dir, make_args=["clean"])

def make(build_dir = None, make_args=[], extra_env={}, check=True):
	"""Builds the proxy with specified flags."""
	env = {}

	env.setdefault("COPT", "")
	env.setdefault("CFLAGS", "")

	env["COPT"] = f"-Werror -Wall {env['COPT']}"
	env["CFLAGS"] = f"-Og -fno-omit-frame-pointer -ggdb3 {env['CFLAGS']}"
	env["CXXFLAGS"] = f"{env['CFLAGS']} {env['COPT']}"

	env.update(extra_env)

	res = run_command(["make"] + make_args, cwd=build_dir, extra_env=env, check=check)

	return res
