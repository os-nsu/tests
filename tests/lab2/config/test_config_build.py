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
    """
    Verify that the static library libconfig.a contains all required configuration functions.
    """

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
        found = False
        for line in symbols:
            if symbol in line:
                if " T " not in line:
                    pytest.fail(
                        f"[ERROR] Symbol '{symbol}' found, but it is not a function.\nDetails: {line}"
                    )
                found = True
                break
        if not found:
            pytest.fail(f"[ERROR] Symbol '{symbol}' not found in libconfig.a.")

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/config/test_config_build.py::test_config_symbols"], scope='session')
def test_config_build(project_dir, test_dir):
    """
    Build the configuration test binaries and verify their existence.
    """
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
            "Ensure the libconfig library is built and linked properly."
        )

    expected_bins = [
        "test_config_parse",
        "test_config_define",
        "test_config_get_set"
    ]
    for bin_name in expected_bins:
        full_path = os.path.join(test_dir, bin_name)
        if not check_file_exists(full_path):
            pytest.fail(f"[ERROR] {bin_name} not found after building in {test_dir}.")
