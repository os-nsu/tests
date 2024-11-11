import pytest
import time
import signal

from steps.proxy_steps import start_proxy, send_signal, build_and_start_proxy
from steps.logger_steps import wait_for_log_message
from entities.proxy import Proxy

def test_proxy_with_empty_config(project_dir, proxy_bin_name, tmp_path, log_file_path):
	empty_config = tmp_path / "empty.conf"
	proxy = Proxy(config_path=empty_config)

	result = build_and_start_proxy(
		project_dir,
		proxy_bin_name,
		log_file_path,
		args=["-c", str(empty_config)],
	)

	assert result.returncode == 0, "Proxy failed to start with an empty config"
	assert "Using default configuration" in result.stdout in result.stderr, "Unexpected behavior with empty config"

def test_proxy_without_config(project_dir, proxy_bin_name, log_file_path):
	result = build_and_start_proxy(
		project_dir,
		proxy_bin_name,
		log_file_path
	)

	assert result.returncode == 0, "Proxy failed to start without config"
	assert "Using default configuration" in result.stdout in result.stderr, "Unexpected behavior without config"

@pytest.mark.parametrize("config_content", [
	'option_without_equals',           # отсутствует знак "="
	'invalid_option = "value"',        # неверная опция
	'correct_option = "missing_quote', # отсутствует закрывающая кавычка
	'correct_option "no_equals"',      # нет знака "="
])
def test_proxy_with_invalid_config(project_dir, proxy_bin_name, tmp_path, config_content, log_file_path):
	invalid_config = tmp_path / "invalid.conf"
	proxy = Proxy(config_path=invalid_config)
	proxy.update_config(config_content)

	result = build_and_start_proxy(
		project_dir,
		proxy_bin_name,
		log_file_path,
		args=["-c", str(invalid_config)]
	)

	assert result.returncode != 0, "Proxy should fail with invalid config"
	assert "Config file error" in result.stderr, "Proxy did not report error for invalid config line ('{config_content}')"

def test_proxy_with_large_config(project_dir, proxy_bin_name, tmp_path, log_file_path):
	large_config = tmp_path / "large.conf"
	proxy = Proxy(config_path=large_config)

	proxy.update_config("\n" * (10 * 1024 * 1024) + 'log_capacity=1024' + "\n" * (10 * 1024 * 1024))

	result = build_and_start_proxy(
		project_dir,
		proxy_bin_name,
		log_file_path,
		args=["-c", str(large_config)]
	)

	assert result.returncode == 0, "Proxy failed to start with large config"
	assert "Configuration loaded successfully" in result.stdout, "Proxy did not handle large config correctly"

@pytest.mark.xfail(reason="SIGHUP handling not yet implemented")
def test_proxy_reload_config(project_dir, proxy_bin_name, tmp_path, proxy_timeout, log_file_path):
	config = tmp_path / "proxy.conf"
	proxy = Proxy(config_path=config)
	proxy.update_config('option="initial_value"')

	proc = start_proxy(project_dir, proxy_bin_name, args=["-c", str(config)])
	time.sleep(proxy_timeout)

	try:
		proxy.update_config('option="new_value"')
		send_signal(proc, signal.SIGHUP)

		assert proxy.has_config_changed(), "Config file modification time did not update after SIGHUP"

		line_number, line_content = wait_for_log_message(
			log_file_path=log_file_path,
			start_position=0,
			message="Configuration reloaded",
			timeout=proxy_timeout
		)

		assert "Configuration reloaded" in line_content, "Proxy did not reload config correctly after SIGHUP"
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy_timeout)
