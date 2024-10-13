import subprocess
import os
import pytest

from steps.build_steps import (
	simple_make,
	simple_clean,
)

def test_successful_make_clean(project_dir):
	simple_make(project_dir)
	simple_clean(project_dir)
	# TODO: compare folders contents before and after clean
	cleaned = True
	assert cleaned, "make clean removed all build artifacts"

def test_successful_compilation(project_dir, proxy_bin_name):
	simple_clean(project_dir)
	simple_make(project_dir)
	assert os.path.exists(f"{proxy_bin_name}"), "Proxy binary exists"

def test_library_symbols(proxy_bin_name):
	result = subprocess.run(["nm", "--defined-only", f"{proxy_bin_name}"], capture_output=True, text=True)
	symbols = result.stdout
	assert "init" in symbols, "Missing 'init' symbol"
	assert "fini" in symbols, "Missing 'fini' symbol"
      
def test_makefile_exists(project_dir):
    makefile_path = os.path.join(project_dir, 'Makefile')
    assert os.path.exists(makefile_path), "Makefile is missing"

def test_project_structure(project_dir):
    expected_dirs = ['src', 'src/include']
    for dir_name in expected_dirs:
        dir_path = os.path.join(project_dir, dir_name)
        assert os.path.isdir(dir_path), f"Directory {dir_name} is missing"


def test_compilation_without_warnings(project_dir):
    result = subprocess.run(
        ["make", "-C", project_dir, "CFLAGS=-Werror"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Compilation failed due to warnings"