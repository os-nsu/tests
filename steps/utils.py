import inspect
import subprocess
import sys

def run_command(args, cwd=None, env=None, timeout=None, check=False):
    """
    Wrapper around subprocess.run that logs the command and its stdout/stderr after execution.
    """
    caller_function = get_caller_function_name()
    marker = f"[TEST SYSTEM][{caller_function}]"

    print(f"{marker} Running command: {' '.join(args)}", file=sys.stdout)

    res = subprocess.run(args, cwd=cwd, env=env, check=check, capture_output=True, text=True, timeout=timeout)

    if res.stdout:
        print(f"{marker} STDOUT:\n{res.stdout}", file=sys.stdout)
    if res.stderr:
        print(f"{marker} STDERR:\n{res.stderr}", file=sys.stderr)


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
    proc = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text)
    return proc


def get_caller_function_name():
    """
    Return the name of the function that called this code;
    if it cannot be determined, return the name of this function.
    """
    stack = inspect.stack()
    if len(stack) > 1:
        return stack[1].function
    return "get_caller_function_name"
