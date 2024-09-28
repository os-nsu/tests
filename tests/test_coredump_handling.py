# tests/test_coredump_handling.py

import subprocess
import pytest
import os

def test_segmentation_fault_handling(proxy_bin_name, project_dir):
    """Tests that a core dump is generated and a stack trace can be printed when the proxy crashes due to a segmentation fault."""    
    
    assert os.path.exists(proxy_bin_name), f"Proxy binary '{proxy_bin_name}' does not exist."
    сoredump_path = os.path.join(project_dir, 'coredump') #где coredump по контракту лежит?

    result = subprocess.run([proxy_bin_name, '--debug-symbols'], cwd=project_dir, capture_output=True, text=True)
    assert result.returncode != 0, "Expected non-zero return code from SIGSEGV"
    assert "Segmentation fault" in result.stderr or "core dumped" in result.stderr, "Expected segmentation fault message"

    assert os.path.exists(сoredump_path), "Coredump was not generated."

    gdb_command = f"gdb --batch -ex 'bt' {proxy_bin_name} {сoredump_path}" #batch чтобы без интерактивного, про ex - без поянтия надо-ли
    gdb_result = subprocess.run(gdb_command, shell=True, capture_output=True, text=True)
    assert "Stacktrace" in gdb_result.stdout or "#0" in gdb_result.stdout, "Failed to obtain stack trace from coredump."
    
