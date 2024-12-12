# steps/utils.py

import inspect
import subprocess
import sys

import pytest

def run_command(args, cwd=None, env=None, timeout=None, check=True, shell=False):
    """
    Wrapper around subprocess.run that logs the command and its stdout/stderr after execution.
    """
    caller_function = get_caller_function_name()
    marker = f"[TEST SYSTEM][{caller_function}]"

    print(f"{marker} Running command: {' '.join(args)}", file=sys.stdout)

    try:
        res = subprocess.run(args, cwd=cwd, env=env, check=False, capture_output=True, text=True, timeout=timeout, shell=shell)
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds: {' '.join(args)}")
        pytest.fail(f"Proxy not finished in {timeout} seconds.")
    except Exception as e:
        print(f"Failed to run command: {' '.join(args)}; Error: {e}")
        pytest.fail(f"Can't start command {' '.join(args)}: {e}")

    if res.stdout:
        print(f"{marker} STDOUT:\n{res.stdout}", file=sys.stdout)
    if res.stderr:
        print(f"{marker} STDERR:\n{res.stderr}", file=sys.stderr)


    if check and res.returncode != 0:
        print(f"Command failed with return code {res.returncode}: {' '.join(args)}")
        pytest.fail(f"Command {' '.join(args)} finished with non-zero return code {res.returncode}.\nStderr: {res.stderr}")

    return res

def start_command(args, cwd=None, env=None, text=True):
    """
    Wrapper around subprocess.Popen that logs the command before starting.
    Unlike run_command, we cannot log stdout/stderr immediately here,
    as the process will still be running. Only the command is logged.
    """
    caller_function = get_caller_function_name()
    marker = f"[TEST SYSTEM][{caller_function}]"

    print(f"{marker} Starting process: {' '.join(args)}", file=sys.stderr)
    try:
        proc = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text)
    except Exception as e:
        print(f"Failed to start process: {' '.join(args)}; Error: {e}")
        pytest.fail(f"Can't start process {' '.join(args)}: {e}")

    return proc


def get_caller_function_name():
    """
    Return the name of the function that called this code;
    if it cannot be determined, return the name of this function.
    """
    stack = inspect.stack()
    if len(stack) > 1:
        return stack[1].function

    return "unknown"