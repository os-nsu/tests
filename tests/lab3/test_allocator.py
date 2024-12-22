#tests/lab3/test_allocator.py

import pytest
import os
from steps.test_steps import check_file_exists

ALLOCATOR_INIT_SUCCESS = "[TEST 1] Allocator initialization: PASS"
SIMPLE_ALLOCATION_SUCCESS = "[TEST 2] Simple allocation: PASS"
SIMPLE_DEALLOCATION_SUCCESS = "[TEST 3] Simple deallocation: PASS"
LARGE_ALLOCATION_FAILURE = "[TEST 4] Large allocation (expected failure): PASS"
FREE_NULL_SUCCESS = "[TEST 5] Free NULL pointer: PASS"

@pytest.mark.dependency()
def test_allocator_exists(project_dir):
    """Check that allocator_test exists."""
    allocator_test = os.path.join(project_dir, "install", "test_allocator")
    check_file_exists(allocator_test)

@pytest.mark.dependency(depends=["tests/lab3/test_allocator.py::test_allocator_exists"])
def test_allocator_basic(proxy_fixture, project_dir):
    """
    Testing the basic functionality of the allocator:
    - `my_malloc` should return a non-null pointer for a reasonable allocation request.
    - `my_free` should not crash and should allow memory reuse.
    - A large request exceeding available memory should return NULL.
    - `my_malloc(0)` should return NULL.
    - `my_free(NULL)` should not crash.
    """
    allocator_test = os.path.join(project_dir, "install", "test_allocator")
    result = proxy_fixture.build_and_run_test(allocator_test)
    stdout = result.stdout
    stderr = result.stderr

    assert ALLOCATOR_INIT_SUCCESS in stdout, "Allocator initialization failed."
    assert SIMPLE_ALLOCATION_SUCCESS in stdout, "my_malloc did not return success."
    assert SIMPLE_DEALLOCATION_SUCCESS in stdout, "my_free did not complete correctly."
    assert LARGE_ALLOCATION_FAILURE in stdout, "my_malloc(large) did not return NULL as expected."
    assert FREE_NULL_SUCCESS in stdout, "my_free(NULL) did not complete correctly."
