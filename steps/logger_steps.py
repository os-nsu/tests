# steps/logger_steps.py

import os
import time

def check_log_file_exists(log_file_path):
    """Check for existing log file."""
    return os.path.exists(log_file_path)

def read_log_from_position(log_file_path, position):
    """Read log file from given position"""
    with open(log_file_path, 'r') as f:
        f.seek(position)
        data = f.read()
        return data

def wait_for_log_message(log_file_path, start_position, message, timeout=1):
    """
    Waits for a message in the log for timeout.
    Returns the position where the message was found.
    """
    end_time = time.time() + timeout
    current_position = start_position
    while time.time() < end_time:
        if not os.path.exists(log_file_path):
            time.sleep(0.1)
            continue
        with open(log_file_path, 'r') as f:
            f.seek(current_position)
            lines = f.readlines()
            for line in lines:
                if message in line:
                    return f.tell()
            current_position = f.tell()
        time.sleep(0.1)
    return None

def clean_log_file(log_file_path):
    """Remove existing log_file"""
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
