# tests/lab2/test_logger.py

import signal
import time
import pytest

from steps.proxy_steps import build_and_run_proxy, send_signal
from steps.logger_steps import check_log_file_exists, wait_for_log_message

def test_log_file_creation(project_dir, proxy_bin_name, proxy_timeout, log_file_path):
	"""Test that log file is created after starting the proxy."""
	proc = build_and_run_proxy(project_dir, proxy_bin_name, log_file_path, proxy_timeout, wait_until_end=False)
	time.sleep(proxy_timeout)
	try:
		assert check_log_file_exists(log_file_path), f"Log file ({log_file_path}) wasn't created after starting the proxy in {proxy_timeout} seconds."
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(proxy_timeout)

@pytest.mark.dependency()
@pytest.mark.parametrize("message, start_position", [
	("Logger initialized", 0),
	("Main loop started", 0)
])
def test_log_contains_message(project_dir, proxy_bin_name, proxy_timeout, message, start_position, log_file_path):
	"""Test that specific messages are presented in the log."""
	proc = build_and_run_proxy(project_dir, proxy_bin_name, log_file_path, proxy_timeout, wait_until_end=False)
	try:
		line_number, line_content = wait_for_log_message(
			log_file_path,
			start_position,
			message,
			timeout=proxy_timeout
		)
		assert message in line_content, f"Message '{message}' wasn't found in log ({log_file_path}), last checked line: {line_number}:{line_content}."
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(proxy_timeout)

@pytest.mark.dependency(depends=["test_log_contains_message"])
def test_log_messages_in_order(project_dir, proxy_bin_name, proxy_timeout, log_file_path):
	"""Test that messages appear in the log in the correct order."""
	messages = ["Logger initialized", "Main loop started"]
	start_position = 0

	proc = build_and_run_proxy(project_dir, proxy_bin_name, log_file_path, proxy_timeout, wait_until_end=True)

	try:
		for message in messages:
			new_position, line = wait_for_log_message(
				log_file_path,
				start_position,
				message,
				timeout=proxy_timeout
			)
			assert message in line, f"Message '{message}' wasn't found in log ({log_file_path}), last checked line: {new_position}:{line}."
			start_position = new_position
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy_timeout)

