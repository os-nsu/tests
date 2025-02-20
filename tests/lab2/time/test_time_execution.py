import os
import re
import pytest
from steps.utils import run_command

EXPECTED_BINARY = "test_time"

@pytest.mark.lab2
@pytest.mark.dependency(depends=[ "tests/lab2/time/test_time_build.py::test_time_symbols_wrapper"
                                 ,"tests/lab2/time/test_time_build.py::test_time_build"],
                        scope="session")
def test_time_execution_wrapper(proxy_bin_dir, current_dir):

    lib_name = "libtime_wrapper.so"

    bin_dir = os.path.join(current_dir, "../", "bin")
    binary_path = os.path.join(bin_dir, EXPECTED_BINARY)

    symlink_path = os.path.join(proxy_bin_dir, "libtime.so")

    library_path = os.path.join(proxy_bin_dir, lib_name)

    os.remove(symlink_path)
    os.symlink(library_path, symlink_path)

    result = run_command([binary_path])

    if result.returncode != 0:
        failed_tests = []
        for line in result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))

        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(f"Unity tests failed in {binary_path} for {lib_name}: {all_failures}")
        else:
            pytest.fail(f"Unity test in {binary_path} for {lib_name} failed, but no specific tests could be identified.")

@pytest.mark.lab2
@pytest.mark.dependency(depends=[ "tests/lab2/time/test_time_build.py::test_time_symbols_syscall"
                                 ,"tests/lab2/time/test_time_build.py::test_time_build"],
                        scope="session")
def test_time_execution_syscall(proxy_bin_dir, current_dir):

    lib_name = "libtime_syscall.so"
    bin_dir = os.path.join(current_dir, "../", "bin")
    binary_path = os.path.join(bin_dir, EXPECTED_BINARY)

    symlink_path = os.path.join(proxy_bin_dir, "libtime.so")

    library_path = os.path.join(proxy_bin_dir, lib_name)

    os.remove(symlink_path)
    os.symlink(library_path, symlink_path)

    result = run_command([binary_path])

    if result.returncode != 0:
        failed_tests = []
        for line in result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))

        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(f"Unity tests failed in {binary_path} for {lib_name}: {all_failures}")
        else:
            pytest.fail(f"Unity test in {binary_path} for {lib_name} failed, but no specific tests could be identified.")

@pytest.mark.lab2
@pytest.mark.dependency(depends=[ "tests/lab2/time/test_time_build.py::test_time_symbols_assembler"
                                 ,"tests/lab2/time/test_time_build.py::test_time_build"],
                        scope="session")
def test_time_execution_assembler(proxy_bin_dir, current_dir):

    lib_name = "libtime_assembler.so"
    bin_dir = os.path.join(current_dir, "../", "bin")
    binary_path = os.path.join(bin_dir, EXPECTED_BINARY)

    symlink_path = os.path.join(proxy_bin_dir, "libtime.so")

    library_path = os.path.join(proxy_bin_dir, lib_name)

    os.remove(symlink_path)
    os.symlink(library_path, symlink_path)

    result = run_command([binary_path])

    if result.returncode != 0:
        failed_tests = []
        for line in result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))

        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(f"Unity tests failed in {binary_path} for {lib_name}: {all_failures}")
        else:
            pytest.fail(f"Unity test in {binary_path} for {lib_name} failed, but no specific tests could be identified.")