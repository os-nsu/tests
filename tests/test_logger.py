# tests/test_logger.py

import os
import time
import signal
import pytest

from steps.proxy_steps import start_proxy, send_signal
from steps.logger_steps import check_log_file_exists, wait_for_log_message
from steps.build_steps import simple_make, simple_clean


def test_log_file_creation(build_proxy, project_dir, proxy_bin_name, proxy_timeout, log_file_path):
    """Test check, that log file is exists."""
    assert check_log_file_exists(log_file_path), "Log file wasn't created after start proxy."

@pytest.mark.parametrize("message, start_position", [
    ("Logger initialized", 0),
    ("Main loop started", 0)])
def test_log_contains_message(build_proxy, clean_log_file, start_proxy_process, proxy_timeout, message, start_position, log_file_path):
    """A parameterized test to check for the existence of a message in the log."""
    new_position = wait_for_log_message(
        log_file_path,
        start_position,
        message,
        timeout=proxy_timeout
    )
    assert new_position is not None, f"Message '{message}' wasn't found in log."


def test_log_messages_in_order(build_proxy, clean_log_file, start_proxy_process, proxy_timeout, log_file_path):
    """The test checks that the messages in the log appear in the correct order."""
    messages = ["Logger initialized", "Main loop started"]
    start_position = 0
    for message in messages:
        new_position = wait_for_log_message(
            log_file_path,
            start_position,
            message,
            timeout=proxy_timeout
        )
        assert new_position is not None, f"Message '{message}' wasn't found in log."
        start_position = new_position

