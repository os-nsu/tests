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

def wait_for_log_message(log_file_path, start_line_num, message, timeout=1):
    """
    Waits for a message in the log file within the specified timeout.
    Returns a tuple (line_number, line_content) where the message was found.
    If the message is not found within the timeout, returns (None, "").
    """
    end_time = time.time() + timeout
    current_line_num = start_line_num

    if not check_log_file_exists(log_file_path):
        while time.time() < end_time:
            if check_log_file_exists(log_file_path):
                break
            time.sleep(0.1)
        else:
            return None, ""
    try:
        with open(log_file_path, 'r') as log_file:
            for _ in range(start_line_num):
                log_file.readline()
            while time.time() < end_time:
                line = log_file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                current_line_num += 1
                if message in line:
                    return current_line_num, line
    except FileNotFoundError:
        return None, ""
    return None, ""

def clean_log_file(log_file_path):
    """Remove existing log_file"""
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
