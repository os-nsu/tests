# tests/lab1/plugins/greeting/test_plugin_greeting_build.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"], scope="session")
def test_plugin_greeting_symbols(project_bin_plugins_dir):
    """
    Verify that the plugin (greeting.so) contains required functions.
    """
    greeting_plugin = os.path.join(project_bin_plugins_dir, "greeting.so")

    required_symbols = ["init", "fini", "name"]
    missing = check_symbols(greeting_plugin, required_symbols)
    if missing:
        pytest.fail(f"The following required symbols are missing or incorrect in greeting.so: {', '.join(missing)}")

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_build.py::test_plugin_greeting_symbols"],
                        scope="session")
@pytest.mark.lab1
def test_plugin_greeting_build(current_dir, proxy_dir):
	build_dir = os.path.join(current_dir, "../", "../")
	make_clean(build_dir=build_dir)
	result = make(build_dir=build_dir, make_args=["plugin_greeting"], extra_env={"PROXY_DIR": proxy_dir}, check=True)
	assert result.returncode == 0, "Plugin greeting tests build failed."