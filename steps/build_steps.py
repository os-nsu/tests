# steps/build_steps.py

import subprocess
import os

def simple_make(project_dir):
	res = subprocess.run(["make"], cwd=project_dir, capture_output=True, check=False)
	assert res.returncode == 0, "make finished with no-zero return code"
	assert len(res.stderr) == 0, f"make has stderr '{res.stderr}'"
	return res

def simple_clean(project_dir):
	res = subprocess.run(["make", "clean"], cwd=project_dir, capture_output=True, check=True)
	assert res.returncode == 0, "make clean finished with no-zero return code"
	assert len(res.stderr) == 0, f"make clean has stderr '{res.stderr}'"
	return res


def make_with_flags(project_dir, cflags):
	"""Builds the proxy with specified flags."""
	env = os.environ.copy()
	env['CFLAGS'] = cflags
	subprocess.run(["make", "clean"], cwd=project_dir, check=True)
	subprocess.run(["make"], cwd=project_dir, env=env, check=True)
