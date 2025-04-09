# steps/utils.py

import inspect
import os
import subprocess
import sys
import pty
import select
import os
import pty
import subprocess
import select
import threading

import pytest

class ProcessResult:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

def read_fd(fd):
    output = []
    while True:
        try:
            r, _, _ = select.select([fd], [], [], 0.1)
            if fd in r:
                data = os.read(fd, 1024).decode()
                if not data:
                    break
                output.append(data)
        except OSError:
            break
    return ''.join(output)

def execute_with_pty(cmd, timeout=None, **kwargs):
    stdout_master, stdout_slave = pty.openpty()
    stderr_master, stderr_slave = pty.openpty()

    try:
        process = subprocess.Popen(
            cmd,
            stdout=stdout_slave,
            stderr=stderr_slave,
            close_fds=True,
            **kwargs
        )
        os.close(stdout_slave)
        os.close(stderr_slave)

        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            raise subprocess.TimeoutExpired(cmd, timeout, output=read_fd(stdout_master), stderr=read_fd(stderr_master))

        stdout = read_fd(stdout_master)
        stderr = read_fd(stderr_master)

        return ProcessResult(process.returncode, stdout, stderr)

    finally:
        os.close(stdout_master)
        os.close(stderr_master)

def run_command(args, cwd=None, extra_env=None, timeout=None, check=True, shell=False):
    """
    Wrapper around execute_with_pty to execute process with pseudo tty.
    """
    caller_function = get_caller_function_name()
    prefix = f"[{caller_function}]"

    print(f"{prefix} Running command: {' '.join(args)}", file=sys.stdout)

    env = os.environ.copy()

    exec_cwd = cwd
    if not exec_cwd:
        exec_cwd = os.getcwd()

    print(f"{prefix} Working directory: {exec_cwd}", file=sys.stdout)

    if extra_env:
        env.update(extra_env)
        env_str = " ".join(f"{k}={extra_env[k]}" for k in sorted(extra_env))
        print(f"{prefix} Environment: {env_str}", file=sys.stdout)

    try:
        res = execute_with_pty(
            args,
            cwd=cwd,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        print(f"{prefix} Command timed out after {timeout} seconds: {' '.join(args)}; Error: {e}")
        pytest.fail(f"Proxy not finished in {timeout} seconds.")
    except Exception as e:
        print(f"{prefix} Failed to run command: {' '.join(args)}; Error: {e}")
        pytest.fail(f"Can't start command {' '.join(args)}: {e}")

    if res.stdout:
        print(f"{prefix} STDOUT:\n{res.stdout}", file=sys.stdout)
    if res.stderr:
        print(f"{prefix} STDERR:\n{res.stderr}", file=sys.stderr)

    if res.returncode != 0:
        print(f"{prefix} Command failed with return code {res.returncode}: {' '.join(args)}")

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
        proc = subprocess.Popen(
            args,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text
        )
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
    if len(stack) > 2:
        return stack[2].function

    return "unknown"

def merge_env(original_env, extra_env, merge_keys=None):
    if merge_keys is None:
        merge_keys = ['LD_LIBRARY_PATH']

    env = original_env.copy()
    for key, value in extra_env.items():
        if key in merge_keys and key in env and env[key]:
            env[key] = value + os.pathsep + env[key]
        else:
            env[key] = value
    return env