# tests/regression/Makefile

CC ?= gcc
CFLAGS ?= -O2 -Wall
BIN_DIR := bin

###############################################################################
# SEGFAULT_MESSAGE
###############################################################################

SEGFAULT_BIN := $(BIN_DIR)/segfault_message

all: $(SEGFAULT_BIN)

$(SEGFAULT_BIN): c_tests/segfault_message.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

###############################################################################
# BIG_WRITE
###############################################################################

BIG_BIN := $(BIN_DIR)/big_write

all: $(BIG_BIN)

$(BIG_BIN): c_tests/big_write.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN_DIR): ; mkdir -p $@
clean: ; rm -rf $(BIN_DIR)
.PHONY: all clean

###############################################################################
# Auxiliary
###############################################################################

$(BIN_DIR):
	mkdir -p $@

clean:
	rm -rf $(BIN_DIR)

.PHONY: all clean
