#tests/lab3/test_cache.py

import pytest
import os
from steps.test_steps import check_file_exists

CONSTRUCT_CACHE_SUCCESS = "[TEST 1] Construct cache: PASS"
CACHE_WRITE_SUCCESS = "[TEST 2] Cache write: PASS"
CACHE_READ_EXISTING_SUCCESS = "[TEST 3] Cache read (existing key): PASS"
CACHE_READ_MISSING_SUCCESS = "[TEST 4] Cache read (missing key): PASS"
CACHE_DESTRUCT_SUCCESS = "[TEST 5] Cache destruct: PASS"

@pytest.mark.dependency()
def test_cache_exists(project_dir):
    """Check that the test executable for cache exists."""
    cache_test = os.path.join(project_dir, "install", "test_cache")
    check_file_exists(cache_test)

@pytest.mark.dependency(depends=["tests/lab3/test_cache.py::test_cache_exists"])
def test_cache_basic(proxy_fixture, project_dir):
    """
    Test basic cache functionality:
    - construct_cache does not crash
    - cache_write successfully writes a key-value pair
    - cache_read successfully reads an existing key
    - Reading a missing key returns NULL
    - destruct_cache works correctly
    """
    cache_test = os.path.join(project_dir, "install", "test_cache")
    result = proxy_fixture.build_and_run_test(cache_test)
    stdout = result.stdout
    stderr = result.stderr

    assert CONSTRUCT_CACHE_SUCCESS in stdout, "construct_cache failed."
    assert CACHE_WRITE_SUCCESS in stdout, "cache_write did not succeed."
    assert CACHE_READ_EXISTING_SUCCESS in stdout, "cache_read failed for an existing key."
    assert CACHE_READ_MISSING_SUCCESS in stdout, "cache_read did not return NULL for a missing key."
    assert CACHE_DESTRUCT_SUCCESS in stdout, "destruct_cache failed."
