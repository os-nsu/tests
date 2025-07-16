# steps/utils.py

import inspect
import os
import subprocess
import sys
import pty
import threading
import pytest
from time import time
from dataclasses import dataclass

@dataclass
class CmdResult:
    returncode: int
    stdout: str
    stderr: str
    t_start: float
    t_end:   float

    @property
    def duration(self) -> float:
        return self.t_end - self.t_start


def _reader(fd: int, bucket: list[bytes]):
    while True:
        try:
            chunk = os.read(fd, 4096)
            if not chunk:
                break
            bucket.append(chunk)
        except OSError:
            break

def execute_with_pty(cmd: list[str], timeout=None, **kwargs) -> CmdResult:

    stdout, stdout_child = pty.openpty()
    stderr, stderr_child = pty.openpty()

    t_start = time()
    proc = subprocess.Popen(
        cmd,
        stdout=stdout_child, stderr=stderr_child,
        close_fds=True,
        **kwargs
    )
    os.close(stdout_child); os.close(stderr_child)

    out_chunks, err_chunks = [], []
    t_out = threading.Thread(target=_reader, args=(stdout, out_chunks))
    t_err = threading.Thread(target=_reader, args=(stderr, err_chunks))
    t_out.start(); t_err.start()

    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.wait()
        raise
    finally:
        t_out.join(); t_out.join()
        os.close(stdout); os.close(stderr)

    t_end = time()

    res = CmdResult(
            returncode=proc.returncode,
            stdout=b"".join(out_chunks).decode(errors="replace"),
            stderr=b"".join(err_chunks).decode(errors="replace"),
            t_start=t_start,
            t_end=t_end,
    )
    return res


def execute_with_pipe(cmd: list[str], timeout, **kwargs) -> CmdResult:
    t_start = time()
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, check=False, **kwargs)
    t_end = time()
    res = CmdResult(
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            t_start=t_start,
            t_end=t_end,
    )
    return res

def run_command(
        cmd: list[str],
        cwd: str | None = None,
        extra_env: dict[str, str] | None = None,
        timeout: int | float | None = None,
        use_pty: bool = True,
    ):
    """
    Wrapper around execute_with_pty to execute process with pseudo tty.
    """
    caller_function = get_caller_function_name()
    prefix = f"[{caller_function}]"

    print(f"{prefix} Running command: {' '.join(cmd)}", file=sys.stdout)

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    try:
        if(use_pty):
            res = execute_with_pty(
                cmd=cmd,
                cwd=cwd,
                env=env,
                timeout=timeout,
            )
        else:
            res = execute_with_pipe(
                cmd=cmd,
                cwd=cwd,
                timeout=timeout,
                env=env
            )
    except subprocess.TimeoutExpired as e:
        print(f"{prefix} Command timed out after {timeout} seconds: {' '.join(cmd)}; Error: {e}")
        pytest.fail(f"Proxy not finished in {timeout} seconds.")
    except Exception as e:
        print(f"{prefix} Failed to run command: {' '.join(cmd)}; Error: {e}")
        pytest.fail(f"Can't start command {' '.join(cmd)}: {e}")

    if res.stdout:
        print(f"{prefix} STDOUT:\n{res.stdout}", file=sys.stdout)
    if res.stderr:
        print(f"{prefix} STDERR:\n{res.stderr}", file=sys.stderr)

    if res.returncode != 0:
        print(f"{prefix} Command failed with return code {res.returncode}: {' '.join(cmd)}")

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