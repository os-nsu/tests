# tests/lab2/test_logger.py

import signal
import time
import pytest

from steps.proxy_steps import send_signal
from steps.logger_steps import check_log_file_exists, wait_for_log_message

def test_log_file_creation(proxy_fixture):
	"""Test that log file is created after starting the proxy."""
<<<<<<< HEAD
	proxy = proxy_fixture
	proc = proxy.build_and_run_proxy(wait_until_end=False)
	time.sleep(proxy.proxy_timeout)
=======
	proc = build_and_run_proxy(
    project_dir=project_dir,
	proxy_bin_name=proxy_bin_name,
	log_file_path=log_file_path,
	proxy_timeout=proxy_timeout,
	wait_until_end=False,
 	check=False
  	)

	time.sleep(proxy_timeout)
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	try:
		assert check_log_file_exists(proxy), f"Log file ({proxy.log_file_path}) wasn't created after starting the proxy in {proxy.proxy_timeout} seconds."
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(proxy.proxy_timeout)

@pytest.mark.dependency()
@pytest.mark.parametrize("message, start_position", [
	("Logger initialized", 0),
	("Main loop started", 0)
])
def test_log_contains_message(proxy_fixture, message, start_position):
	"""Test that specific messages are presented in the log."""
<<<<<<< HEAD
	proxy = proxy_fixture
	proc = proxy.build_and_run_proxy(wait_until_end=False)
=======
	proc = build_and_run_proxy(
    project_dir=project_dir,
    proxy_bin_name=proxy_bin_name,
    log_file_path=log_file_path,
    proxy_timeout=proxy_timeout,
    wait_until_end=False,
    check=False
    )

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	try:
		line_number, line_content = wait_for_log_message(
			proxy,
			start_position,
			message
		)
		assert message in line_content, f"Message '{message}' wasn't found in log ({proxy.log_file_path}), last checked line: {line_number}:{line_content}."
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(proxy.proxy_timeout)

@pytest.mark.dependency(depends=["test_log_contains_message"])
def test_log_messages_in_order(proxy_fixture):
	"""Test that messages appear in the log in the correct order."""
	proxy = proxy_fixture
	messages = ["Logger initialized", "Main loop started"]
	start_position = 0

<<<<<<< HEAD
	proc = proxy.build_and_run_proxy(wait_until_end=True)
=======
	proc = build_and_run_proxy(
    project_dir=project_dir,
    proxy_bin_name=proxy_bin_name,
    log_file_path=log_file_path,
    proxy_timeout=proxy_timeout,
    wait_until_end=False,
    check=False
    )
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)

	try:
		for message in messages:
			new_position, line = wait_for_log_message(
				proxy,
				start_position,
				message
			)
			assert message in line, f"Message '{message}' wasn't found in log ({proxy.log_file_path}), last checked line: {new_position}:{line}."
			start_position = new_position
	finally:
		send_signal(proc, signal.SIGINT)
		proc.wait(proxy.proxy_timeout)

