# tests/lab2/time/test_time_build.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/time/test_time_file_structure.py::test_time_files_exists[libtime_wrapper.so]"], scope="session")
def test_time_symbols_wrapper(proxy_bin_dir):
    """
    Check that the 'get_time' symbol exists in libtime_wrapper.so and is of the correct type.
    """
    lib_name = "libtime_wrapper.so"

    libtime_path = os.path.join(proxy_bin_dir, "libtime_wrapper.so")

    required_symbols = ["get_time"]

    missing = check_symbols(libtime_path, required_symbols)
    if missing:
        pytest.fail(f"The following required symbols are missing or incorrect in {lib_name}: {', '.join(missing)}")

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/time/test_time_file_structure.py::test_time_files_exists[libtime_syscall.so]"], scope="session")
def test_time_symbols_syscall(proxy_bin_dir):
    """
    Check that the 'get_time' symbol exists in libtime_syscall.so and is of the correct type.
    """
    lib_name = "libtime_syscall.so"

    libtime_path = os.path.join(proxy_bin_dir, lib_name)

    required_symbols = ["get_time"]

    missing = check_symbols(libtime_path, required_symbols)
    if missing:
        pytest.fail(f"The following required symbols are missing or incorrect in {lib_name}: {', '.join(missing)}")

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/time/test_time_file_structure.py::test_time_files_exists[libtime_assembler.so]"], scope="session")
def test_time_symbols_assembler(proxy_bin_dir):
    """
    Check that the 'get_time' symbol exists in libtime_assembler.so and is of the correct type.
    """
    lib_name = "libtime_assembler.so"

    libtime_path = os.path.join(proxy_bin_dir, lib_name)

    required_symbols = ["get_time"]

    missing = check_symbols(libtime_path, required_symbols)
    if missing:
        pytest.fail(f"The following required symbols are missing or incorrect in {lib_name}: {', '.join(missing)}")

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/time/test_time_file_structure.py::test_time_files_exists[libtime.so]"], scope="session")
def test_time_symlink(proxy_bin_dir):
    """
    Checks that the symbolic link 'libtime.so' points to one of the versions of the library.
    """
    symlink_name = "libtime.so"
    symlink_path = os.path.join(proxy_bin_dir, symlink_name)
    target_path = os.readlink(path=symlink_path)

    expected_targets = [
        "./libtime_assembler.so",
        "./libtime_syscall.so",
        "./libtime_wrapper.so"
    ]

    if target_path not in expected_targets:
        pytest.fail(f"SymLink {symlink_name} points to an incorrect target: {target_path}. Expected one of {expected_targets}.")

@pytest.mark.dependency(depends=[
    f"tests/lab2/time/test_time_build.py::test_time_symlink",
    ],
    scope="session")
@pytest.mark.lab2
def test_time_build(current_dir, proxy_dir):
    """
    Building tests for my_time library
    """
    build_dir = os.path.join(current_dir, "../")
    make_clean(build_dir=build_dir)
    result = make(build_dir=build_dir, make_args=["time"], extra_env={"PROXY_DIR": proxy_dir}, check=True)
    assert result.returncode == 0, "Tests for my_time build failed."