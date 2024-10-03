import subprocess
import pytest

from steps.proxy_steps import (
	start_proxy,
)

def test_successful_start(project_dir, proxy_bin_name):
	start_proxy(project_dir, proxy_bin_name)
	# TODO: print backtrace if coredump was generated
