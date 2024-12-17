# tests/lab1/test_build.py

import os
import pytest

from steps.build_steps import (
	simple_make,
	simple_clean,
)
from steps.test_steps import (
    check_file_exists
)
from steps.utils import run_command
# -------------------------------------
# Tests for the static library
# -------------------------------------

@pytest.mark.dependency(depends=[
    "tests/lab1/test_file_structure.py::test_files_exist[Makefile]",
    "tests/lab1/test_file_structure.py::test_directories_exist[src]",
    "tests/lab1/test_file_structure.py::test_directories_exist[src/backend]",
    "tests/lab1/test_file_structure.py::test_files_exist[src/backend/static_lib.c]",
    "tests/lab1/test_file_structure.py::test_files_exist[src/backend/master.c]"
], scope='session')
def test_static_library_compilation(project_dir, master_bin_name):
    """Test that the master and static library compile successfully."""
    simple_clean(project_dir)
    simple_make(project_dir)

    check_file_exists(master_bin_name)

@pytest.mark.dependency(depends=["test_static_library_compilation"])
def test_static_library_inclusion(project_dir, master_bin_name):
    """Test that the static library function is included in the proxy executable."""
    simple_clean(project_dir)
    simple_make(project_dir)

    result = run_command(["nm", "--defined-only", master_bin_name], cwd=project_dir, check=True)

    symbols = result.stdout
    assert "hello_from_static_lib" in symbols, "Function 'hello_from_static_lib' not found in master binary symbols."

# -------------------------------------
# Tests for the dynamic library
# -------------------------------------

@pytest.mark.dependency(depends=[
    "tests/lab1/test_build.py::test_static_library_compilation",
    "tests/lab1/test_file_structure.py::test_files_exist[src/backend/dynamic_lib.c]",],
                        scope="session")
def test_dynamic_library_compilation(project_dir):
    """Test that the dynamic library compiles successfully."""
    simple_clean(project_dir)
    simple_make(project_dir)

    dynamic_lib = os.path.join(project_dir, 'install', 'libdynamic.so')

    check_file_exists(dynamic_lib)

@pytest.mark.dependency(depends=["test_dynamic_library_compilation"])
def test_dynamic_library_dependencies(project_dir, master_bin_name):
    """Test that the dynamic library links to proxy executable."""
    simple_clean(project_dir)
    simple_make(project_dir)

    result = run_command(["ldd", master_bin_name], cwd=project_dir, check=True)

    dependencies = result.stdout
    assert "libdynamic.so" in dependencies, "Dynamic library 'libdynamic.so' not found in master binary dependencies."

# -------------------------------------
# Tests for the plugin
# -------------------------------------

@pytest.mark.dependency(depends=[
    "tests/lab1/test_build.py::test_dynamic_library_compilation",
    "tests/lab1/test_file_structure.py::test_directories_exist[contrib]",
    "tests/lab1/test_file_structure.py::test_directories_exist[contrib/plugin]",
    "tests/lab1/test_file_structure.py::test_files_exist[contrib/plugin/plugin.c]"],
                        scope="session")
def test_plugin_compilation(project_dir, plugin_bin_name):
    """Test that the plugin compiles successfully."""
    simple_clean(project_dir)
    simple_make(project_dir)

    check_file_exists(plugin_bin_name)
