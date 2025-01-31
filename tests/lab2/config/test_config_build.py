# tests/lab2/config/test_config_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command

@pytest.mark.lab2
@pytest.mark.dependency(
    depends=["tests/lab1/config/test_config_build.py::test_config_symbols"],
    scope="session"
)
def test_config_symbols(project_bin_dir):
    libconfig = os.path.join(project_bin_dir, "libconfig.a")

    res = run_command(["nm", "--defined-only", libconfig], cwd=project_bin_dir, check=True)
    symbols = res.stdout.splitlines()

    required_symbols = [
        "create_config_table",
        "destroy_config_table",
        "parse_config",
        "define_variable",
        "get_variable",
        "set_variable",
        "does_variable_exist"
    ]

    for symbol in required_symbols:
        for line in symbols:
            if symbol in line:
                if " T " not in line:
                    pytest.fail(
                        f"[ERROR] Symbol '{symbol}' found, but it is not a function.\n"
                        f"Details: {line}"
                    )
                break
        else:
            pytest.fail(f"[ERROR] Symbol '{symbol}' not found in libconfig.a.")

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/config/test_config2_build.py::test_config2_symbols"], scope='session')
def test_config_build(project_dir, test_dir):
    simple_clean(test_dir)

    make_result = make(
        project_dir=test_dir,
        make_args=["all"],
        extra_env={"PROXY_DIR": project_dir},
        check=True
    )

    if make_result.returncode != 0:
        pytest.fail(
            "[ERROR] Unable to build tests for config.\n"
            "Please ensure all required libraries (e.g., 'libconfig') are installed and accessible."
        )

    expected_bins = [
        "test_config_parse",
    ]
    for bin_name in expected_bins:
        if not check_file_exists(os.path.join(test_dir, bin_name)):
            pytest.fail(f"[ERROR] {bin_name} not found after building.")
