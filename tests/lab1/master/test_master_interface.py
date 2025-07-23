# tests/lab1/config/test_config_build.py

import pytest
from steps.build_steps import make

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_master_config_symbols",
                                 "tests/lab1/master/test_master_build.py::test_master_logger_symbols"],
                        scope="session")
@pytest.mark.lab1
def test_master_interface(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_master_interface"
    res = make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)

    make_code = res.returncode
    assert make_code == 0, f"Interfaces match expected, see stderr"
