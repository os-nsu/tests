import pytest
import time
import signal

from steps.proxy_steps import run_proxy, send_signal, build_and_run_proxy
from steps.logger_steps import wait_for_log_message
from entities.proxy import Proxy

def test_proxy_with_empty_config(proxy_fixture):
	proxy = proxy_fixture
	proxy.config_path = proxy.tmp_path / "empty.conf"

	result = proxy.build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=False
	)

	result.wait()
	stdout, stderr = result.communicate()

	assert result.returncode == 0, "Proxy failed to start with an empty config"
	assert "Using default configuration" in stdout, "Unexpected behavior with empty config"

def test_proxy_without_config(proxy_fixture):
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=False)

	result.wait()
	stdout, stderr = result.communicate()

	assert result.returncode == 0, "Proxy failed to start without config"
	assert "Using default configuration" in stdout, "Unexpected behavior without config"

@pytest.mark.parametrize("config_content", [
	'option_without_equals',           # without "="
	'invalid_option = "value"',        # invalid_option
	'correct_option = "missing_quote', # missing quote
	'correct_option "no_equals"',      # no "="
])
def test_proxy_with_invalid_config(proxy_fixture, config_content):
	proxy = proxy_fixture
	proxy.config_path = proxy.tmp_path / "invalid.conf"
	proxy.update_config(config_content)

	result = proxy.build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=False
	)

	result.wait()
	stdout, stderr = result.communicate()

	assert result.returncode != 0, "Proxy should fail with invalid config"
	assert "Config file error" in stderr, "Proxy did not report error for invalid config line ('{config_content}')"

def test_proxy_with_large_config(proxy_fixture):
	proxy = proxy_fixture
	proxy.config_path = proxy.tmp_path / "large.conf"

	proxy.update_config("\n" * (10 * 1024 * 1024) + 'log_capacity=1024' + "\n" * (10 * 1024 * 1024))

	result = build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=False
	)

	result.wait()
	stdout, stderr = result.communicate()

	assert result.returncode == 0, "Proxy failed to start with large config"
	assert "Configuration loaded successfully" in stdout, "Proxy did not handle large config correctly"

@pytest.mark.xfail(reason="SIGHUP handling not yet implemented")
def test_proxy_reload_config(proxy_fixture):
	proxy = proxy_fixture
	proxy.config_path = proxy.tmp_path / "proxy.conf"
	proxy.update_config('option="initial_value"')

	proc = run_proxy(args=["-c", str(proxy.config_path)], wait_until_end=False)
	time.sleep(proxy.proxy_timeout)

	try:
		proxy.update_config('option="new_value"')
		send_signal(proc, signal.SIGHUP)

		assert proxy.has_config_changed(), "Config file modification time did not update after SIGHUP"

		line_number, line_content = wait_for_log_message(
			log_file_path=proxy.log_file_path,
			start_position=0,
			message="Configuration reloaded",
			timeout=proxy.proxy_timeout
		)

		assert "Configuration reloaded" in line_content, "Proxy did not reload config correctly after SIGHUP"
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy.proxy_timeout)
