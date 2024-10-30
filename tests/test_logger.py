# tests/test_logger.py

import os
import time
import signal
import pytest

from steps.proxy_steps import build_and_start_proxy, start_proxy, send_signal
from steps.logger_steps import check_log_file_exists, clean_log_file, wait_for_log_message
from steps.build_steps import simple_make, simple_clean


def test_log_file_creation(project_dir, proxy_bin_name, proxy_timeout, log_file_path):
    """Test that log file is created after starting the proxy."""
    proc = build_and_start_proxy(project_dir, proxy_bin_name, proxy_timeout, log_file_path)

    try:
        assert check_log_file_exists(log_file_path), "Log file wasn't created after starting the proxy."
    finally:
        send_signal(proc, signal.SIGINT)
        proc.wait(timeout=proxy_timeout)

@pytest.mark.parametrize("message, start_position", [
    ("Logger initialized", 0),
    ("Main loop started", 0)
])
def test_log_contains_message(project_dir, proxy_bin_name, proxy_timeout, message, start_position, log_file_path):
    """Test that specific messages are presented in the log."""
    proc = build_and_start_proxy(project_dir, proxy_bin_name, proxy_timeout, log_file_path)

    try:
        new_position = wait_for_log_message(
            log_file_path,
            start_position,
            message,
            timeout=proxy_timeout
        )
        assert new_position is not None, f"Message '{message}' wasn't found in log."
    finally:
        send_signal(proc, signal.SIGINT)
        proc.wait(timeout=proxy_timeout)


def test_log_messages_in_order(project_dir, proxy_bin_name, proxy_timeout, log_file_path):
    """Test that messages appear in the log in the correct order."""
    messages = ["Logger initialized", "Main loop started"]
    start_position = 0

    proc = build_and_start_proxy(project_dir, proxy_bin_name, proxy_timeout, log_file_path)

    try:
        for message in messages:
            new_position = wait_for_log_message(
                log_file_path,
                start_position,
                message,
                timeout=proxy_timeout
            )
            assert new_position is not None, f"Message '{message}' wasn't found in log."
            start_position = new_position
    finally:
        send_signal(proc, signal.SIGINT)
        proc.wait(timeout=proxy_timeout)

