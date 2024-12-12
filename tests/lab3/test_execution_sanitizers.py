# tests/lab3/test_execution_sanitizers.py

import subprocess
import pytest
import time
import signal

from steps.proxy_steps import send_signal

@pytest.mark.parametrize("sanitizer", [
	("address"),
	("undefined")
])
def test_execution_with_sanitizers(proxy_fixture, sanitizer):
	"""Tests the launch of a proxy built with AddressSanitizer and UndefinedBehaviorSanitizer."""

	extra_env = {}
	extra_env["SANITIZER_FLAGS"] = f"-fsanitize={sanitizer}"
	extra_env["SANITIZER_OPTIONS"] = "detect_leaks=0:abort_on_error=1:disable_coredump=0"
	extra_env["CFLAGS"] = f"{extra_env['SANITIZER_FLAGS']} -fno-sanitize-recover=all -fstack-protector-all"
	extra_env["LDFLAGS"] = f"{extra_env['SANITIZER_FLAGS']}"
	extra_env["ASAN_OPTIONS"] = f"{extra_env['SANITIZER_OPTIONS']}:detect_stack_use_after_return=0:check_initialization_order=1:strict_init_order=1"
	extra_env["UBSAN_OPTIONS"] = f"{extra_env['SANITIZER_OPTIONS']}"

<<<<<<< HEAD
	proxy = proxy_fixture
	proc = proxy.build_and_run_proxy(extra_env=extra_env, wait_until_end=False)
	time.sleep(proxy.proxy_timeout)
=======
	proc = build_and_run_proxy(
    project_dir=project_dir,
    proxy_bin_name=proxy_bin_name,
    extra_env=extra_env,
    wait_until_end=False,
    check=False
    )

	time.sleep(proxy_timeout)

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy.proxy_timeout)
		stdout, stderr = proc.communicate(timeout=proxy.proxy_timeout)
		expected_returncode = -signal.SIGINT
		assert proc.returncode == expected_returncode, f"Proxy finish with code {proc.returncode} after SIGINT, expected {expected_returncode}."
		assert stderr == ""
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("The proxy not terminate within the specified time after SIGINT.")