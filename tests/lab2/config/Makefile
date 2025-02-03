# tests/lab2/config/Makefile

MAINDIR ?= $(shell pwd)

CC = gcc
CFLAGS ?= -Wall -Wextra -O2
LDFLAGS = -L$(PROXY_DIR)/install -lconfig

ALL_TESTS = test_parse_config test_define_variable test_does_variable_exist \
            test_get_variable test_set_variable

all: $(ALL_TESTS)

test_parse_config: c_tests/test_parse_config.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

test_define_variable: c_tests/test_define_variable.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

test_does_variable_exist: c_tests/test_does_variable_exist.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

test_get_variable: c_tests/test_get_variable.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

test_set_variable: c_tests/test_set_variable.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)
clean:
	rm -f $(ALL_TESTS)
