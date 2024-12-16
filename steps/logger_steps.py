# steps/logger_steps.py

import os
import time

def check_log_file_exists(proxy):
    """Check for existing log file."""
    return os.path.exists(proxy.log_file_path)

def read_log_from_position(proxy, position):
    """Read log file from given position"""
    with open(proxy.log_file_path, 'r') as f:
        f.seek(position)
        data = f.read()
        return data

def wait_for_log_message(proxy,start_line_num, message,):
    """
    Waits for a message in the log file within the specified timeout.
    Returns a tuple (line_number, line_content) where the message was found.
    If the message is not found within the timeout, returns (None, "").
    """
    end_time = time.time() + proxy.proxy_timeout
    current_line_num = start_line_num
    line = ''

    if not check_log_file_exists(proxy):
        while time.time() < end_time:
            if check_log_file_exists(proxy):
                break
            time.sleep(0.1)
        else:
            return current_line_num, line
    try:
        with open(proxy.log_file_path, 'r') as log_file:
            for _ in range(start_line_num):
                if log_file.readline() == '':
                    break
            while time.time() < end_time:
                line = log_file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                current_line_num += 1
                if message in line:
                    return current_line_num, line.rstrip()
    except FileNotFoundError:
        return current_line_num, line
    return current_line_num, line

def clean_log_file(proxy):
    """Remove existing log_file"""
    if os.path.exists(proxy.log_file_path):
        os.remove(proxy.log_file_path)
