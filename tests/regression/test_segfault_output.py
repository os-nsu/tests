# tests/regression/test_segfault_output.py

import os
import pytest
from steps.utils import run_command
from steps.build_steps import make, make_clean

@pytest.mark.regression
def test_segfault_message(set_cwd_to_test_file_dir):
    make_clean()
    make(check=True)

    bin_path = os.path.join("bin", "segfault_message")

    res = run_command([bin_path], timeout=3, check=False)

    assert "SEGFAULT-LINE" in res.stdout, "lose stdout because buffering"
    assert res.returncode != 0
