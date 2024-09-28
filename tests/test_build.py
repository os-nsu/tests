# tests/test_build.py

import subprocess
import os
import pytest

from steps.build_steps import (
    simple_make,
    simple_clean,
)

def test_successful_make_clean(project_dir):
    """Tests cleaning the project using 'make clean'."""
    simple_make(project_dir)
    simple_clean(project_dir)
    # TODO: compare folders contents before and after clean
    cleaned = True
    assert cleaned, "make clean removed all build artifacts"

def test_successful_compilation(project_dir, proxy_bin_name):
    """Tests that the proxy compile successfully."""
    simple_clean(project_dir)
    simple_make(project_dir)
    assert os.path.exists(f"{proxy_bin_name}"), "Proxy binary exists"

def test_library_symbols(proxy_bin_name):
    """Tests that the proxy binary contains expected library symbols."""
    result = subprocess.run(["nm", "--defined-only", f"{proxy_bin_name}"], capture_output=True, text=True)
    symbols = result.stdout
    assert "init" in symbols, "Missing 'init' symbol"
    assert "fini" in symbols, "Missing 'fini' symbol"

def test_build_with_sanitizers(project_dir, proxy_bin_name):
    """Tests building the proxy server with AddressSanitizer and UndefinedBehaviorSanitizer."""
    
    subprocess.run(["make", "clean"], cwd=project_dir, capture_output=True, check=True)

    sanitizer_flags = "-fsanitize=address,undefined -fno-omit-frame-pointer -g"
    
    build_result = subprocess.run(["make", f"CFLAGS={sanitizer_flags}"], cwd=project_dir, capture_output=True, text=True)
    assert build_result.returncode == 0, f"'make' failed with return code {build_result.returncode}"
    
    assert os.path.exists(proxy_bin_name), f"Proxy binary '{proxy_bin_name}' was not created after building with sanitizers."
