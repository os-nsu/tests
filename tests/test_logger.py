# tests/test_logger.py

import os
import time
import signal
import pytest

from steps.proxy_steps import start_proxy, send_signal
from steps.logger_steps import check_log_file_exists, wait_for_log_message
from steps.build_steps import simple_make, simple_clean

@pytest.fixture(scope="module")
def build_proxy(project_dir):
    """Build proxy before tests."""
    simple_clean(project_dir)
    simple_make(project_dir)

@pytest.fixture
def clean_log_file(log_file_path):
    """Delete log file before test."""
    if os.path.exists(log_file_path):
        os.remove(log_file_path)


@pytest.fixture
def start_proxy_process(project_dir, proxy_bin_name, proxy_timeout):
    """Start proxy before test and finish after test."""
    proc = start_proxy(project_dir, proxy_bin_name)
    time.sleep(proxy_timeout)
    yield proc
    send_signal(proc, signal.SIGINT)
    proc.wait(timeout=proxy_timeout)

def test_log_file_creation(build_proxy, project_dir, proxy_bin_name, proxy_timeout, log_file_path):
    """ТTest check, that log file is exists."""
    assert check_log_file_exists(log_file_path), "Log file wasn't created after start proxy."

@pytest.mark.parametrize("message, start_position", [
    ("ready to accept connections", 0),
    ("new client connected", 0)])
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
    messages = ["ready to accept connections", "new client connected"]
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

