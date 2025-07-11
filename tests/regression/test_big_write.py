# tests/regression_big/test_big_write.py

import os, pytest
from steps.build_steps import make, make_clean
from steps.utils import run_command

HERE = os.path.dirname(__file__)

@pytest.mark.regression
def test_big_continuous_write(set_cwd_to_test_file_dir):
    make_clean(build_dir=HERE)
    make(build_dir=HERE, check=True)

    exe = os.path.join(HERE, "bin", "big_write")

    res = run_command([exe], timeout=3, check=False)
    assert len(res.stdout) > 200000, "TTY-deadlock: can't read stdout"
    assert res.returncode == 0
