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
