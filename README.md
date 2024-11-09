## Tests for nsu os proxy

Tests are written using pytest framework.

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Running tests

To view all available options and understand how to use the test runner, use the --help flag
Example
```bash
./run_tests.py --help
```

Example
```bash
./run_tests.py --src ../proxy-grisha
```

To run tests only for a specific laboratory(or multiple laboratory) work, use the --lab-num argument followed by the lab number(or numbers).
Example: Run tests for lab 1.
```bash
./run_tests.py --lab-num 1 --src ../proxy-grisha
```

Example: Run tests for Lab 1 and Lab 2.
```bash
./run_tests.py --lab-num 1 2 --src ../proxy-grisha
```

Example: Run tests for Lab 1, Lab 2, and Lab 4.
```bash
./run_tests.py --lab-num 1 2 4 --src ../proxy-grisha
```
