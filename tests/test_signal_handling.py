# tests/test_signal_handling.py

import subprocess
import pytest
import signal
import time

timeout_size = 5

def test_termination_on_sigint(proxy_bin_name):
    """Tests that the proxy correctly terminates upon receiving SIGINT."""
    proc = subprocess.Popen([proxy_bin_name])
    time.sleep(1) #Наверное надо придумать что-то получше.
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=timeout_size)
    except subprocess.TimeoutExpired:
        proc.kill()
        pytest.fail(f"Proxy did not terminate within {timeout_size} seconds after SIGINT")
    assert proc.returncode == 0, f"Proxy exited with code {proc.returncode} after SIGINT, expected 0"

def test_termination_on_sigquit(proxy_bin_name):
    """Tests that the proxy correctly terminates upon receiving SIGQUIT."""
    proc = subprocess.Popen([proxy_bin_name])
    time.sleep(1) #Наверное надо придумать что-то получше.
    proc.send_signal(signal.SIGQUIT)
    try:
        proc.wait(timeout=timeout_size)
    except subprocess.TimeoutExpired:
        proc.kill()
        pytest.fail(f"Proxy did not terminate within {timeout_size} seconds after SIGQUIT")
    assert proc.returncode == 0, f"Proxy exited with code {proc.returncode} after SIGQUIT, expected 0"

