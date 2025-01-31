# tests/lab2/config/Makefile

MAINDIR ?= $(shell pwd)
CC = gcc

LDFLAGS = -L$(PROXY_DIR)/install -lconfig

ALL_TESTS = test_config2_parse \

all: $(ALL_TESTS)

test_config2_parse: test_config2_parse.c
	$(CC) $(COPT) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(ALL_TESTS)
