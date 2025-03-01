import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols

@pytest.mark.lab2
@pytest.mark.dependency(
    depends=["tests/lab2/logger/test_lab2_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
    scope='session'
)
def test_logger_symbols(proxy_bin_dir):
    liblogger_path = os.path.join(proxy_bin_dir, "liblogger.so")

    required_symbols = ["write_log"]

    missing = check_symbols(liblogger_path, required_symbols)
    if missing:
        pytest.fail(
            f"The following required symbols are missing or incorrect in liblogger.so: {', '.join(missing)}"
        )

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/logger/test_lab2_logger_build.py::test_logger_symbols"],
                        scope="session")
def test_logger_build(current_dir, proxy_dir):
    build_dir = os.path.join(current_dir, "../")
    make_clean(build_dir=build_dir)
    result = make(
        build_dir=build_dir,
        make_args=["logger"],
        extra_env={"PROXY_DIR": proxy_dir},
        check=True
    )
    assert result.returncode == 0, "Logger tests build failed."
