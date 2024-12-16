import pytest
import time
import signal
import os

from steps.proxy_steps import send_signal
from steps.logger_steps import wait_for_log_message

def test_proxy_with_empty_config(proxy_fixture):
	proxy = proxy_fixture
	with open(proxy.config_path, 'w') as f:
		f.write('')
	result = proxy.build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=True
	)

	assert result.returncode == 0, "Proxy failed to start with an empty config"

def test_proxy_without_config(proxy_fixture):
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=True)

	assert result.returncode == 0, "Proxy failed to start without config"

@pytest.mark.parametrize("config_content", [
	'option_without_equals',           # without "="
	'invalid_option = "value"',        # invalid_option
	'correct_option = "missing_quote', # missing quote
	'correct_option "no_equals"',      # no "="
])
def test_proxy_with_invalid_config(proxy_fixture, config_content, tmp_path):
	proxy = proxy_fixture
	with open(proxy.config_path, 'w') as f:
			f.write('')
	proxy.update_config(config_content)

	result = proxy.build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=True
	)

	assert result.returncode != 0, "Proxy should fail with invalid config"

def test_proxy_with_large_config(proxy_fixture):
	proxy = proxy_fixture
	with open(proxy.config_path, 'w') as f:
		f.write('')

	proxy.update_config("\n" * (10 * 1024 * 1024) + 'log_capacity=1024' + "\n" * (10 * 1024 * 1024))

	result = proxy.build_and_run_proxy(
		args=["-c", str(proxy.config_path)],
		wait_until_end=True
	)

	assert result.returncode == 0, "Proxy failed to start with large config"

@pytest.mark.xfail(reason="SIGHUP handling not yet implemented")
def test_proxy_reload_config(proxy_fixture):
	proxy = proxy_fixture
	with open(proxy.config_path, 'w') as f:
		f.write('')
	proxy.update_config('option="initial_value"')

	proc = proxy.build_and_run_proxy(args=["-c", str(proxy.config_path)], wait_until_end=True)
	time.sleep(proxy.proxy_timeout)

	try:
		proxy.update_config('option="new_value"')
		send_signal(proc, signal.SIGHUP)

		assert proxy.has_config_changed(), "Config file modification time did not update after SIGHUP"

		line_number, line_content = wait_for_log_message(
			proxy = proxy,
			start_position=0,
			message="Configuration reloaded"
		)

		assert "Configuration reloaded" in line_content, "Proxy did not reload config correctly after SIGHUP"
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy.proxy_timeout)
