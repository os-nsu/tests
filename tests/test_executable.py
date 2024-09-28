# tests/test_executable.py

import subprocess
import pytest

from steps.proxy_steps import (
	start_proxy,
)

def test_successful_start(project_dir, proxy_bin_name):
    """Tests running proxy successfully."""           
    start_proxy(project_dir, proxy_bin_name)
	# TODO: print backtrace if coredump was generated


def test_run_without_arguments(proxy_bin_name):
    """Tests that the proxy starts successfully without arguments"""
    result = subprocess.run([f"{proxy_bin_name}"], capture_output=True, text=True)
    assert result.returncode == 0, f"Proxy exited with code {result.returncode} without arguments"
    assert result.stderr == "", f"Proxy exited with error: {result.stderr}"
        
def test_run_with_help_argument(proxy_bin_name):
    """Tests running the proxy successfully with '--help' argument."""
    result = subprocess.run([proxy_bin_name, '--help'], capture_output=True, text=True)
    assert result.returncode == 0, f"Proxy exited with code {result.returncode} with '--help' argument"
    assert "Name" in result.stdout or "usage" in result.stdout, "Expected usage information in output"

def test_run_with_invalid_arguments(proxy_bin_name):
    """Tests running the proxy with invalid arguments."""
    result = subprocess.run([proxy_bin_name, '--invalid_arg', '--very_invalid_arg'], capture_output=True, text=True)
    assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments"
    assert "Invalid argument" in result.stderr or "unknown option" in result.stderr, "Expected error message for invalid argument"
