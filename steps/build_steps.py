import subprocess

def simple_make(project_dir):
	res = subprocess.run(["make"], cwd=project_dir, capture_output=True, check=True)
	assert res.returncode == 0, "make finished with no-zero return code"
	assert res.stderr == "", f"make has stderr"
	return res

def simple_clean(project_dir):
	res = subprocess.run(["make", "clean"], cwd=project_dir, capture_output=True, check=True)
	assert res.returncode == 0, "make clean finished with no-zero return code"
	assert res.stderr == "", f"make clean has stderr"
	return res
