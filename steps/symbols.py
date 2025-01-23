# steps/symbols.py

from steps.utils import run_command

def check_symbols(binary_path, required_symbols, cwd=None):
    res = run_command(["nm", "--defined-only", binary_path], cwd=cwd, check=True)
    lines = res.stdout.splitlines()
    missing = []

    for sym in required_symbols:
        found_symbol = False

        for line in lines:
            parts = line.split()
            if len(parts) < 3:
                continue

            address, symbol_type, symbol_name = parts[0], parts[1], parts[2]

            if symbol_name == sym:
                found_symbol = True

                if symbol_type != 'T':
                    missing.append(f"{sym} (incorrect type: {line})")
                break

        if not found_symbol:
            missing.append(sym)
    return missing