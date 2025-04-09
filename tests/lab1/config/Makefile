# File: tests/lab1/config/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

# Proxy
PROXY_DIR ?= $(shell pwd)
PROXY_INC := -I$(PROXY_DIR)/src/include

# Unity
UNITY_DIR  := ../../common/unity
UNITY_INC  := -I$(UNITY_DIR)
UNITY_SRC  := $(UNITY_DIR)/unity.c

# Path to libconfig.a
LDFLAGS_CONFIG := -L$(PROXY_DIR)/install -lconfig

# Where your test .c sources are
TEST_SRC_DIR  := c_tests

# Where to place compiled test binaries
BIN_DIR := bin

###############################################################################
# test_config_create_config_table
###############################################################################

CREATE_TARGET = test_config_create_config_table

TEST_CREATE = $(TEST_SRC_DIR)/$(CREATE_TARGET).c

BIN_CREATE = $(BIN_DIR)/$(CREATE_TARGET)

$(CREATE_TARGET): $(BIN_CREATE)
	@echo "[OK] Built $@ => $<"

$(BIN_CREATE): $(TEST_CREATE) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_CREATE)"
	$(CC) $(CFLAGS) $(PROXY_INC) $(UNITY_INC) -o $@ $(TEST_CREATE) $(UNITY_SRC) $(LDFLAGS_CONFIG)

clean_$(CREATE_TARGET):
	rm -rf $(BIN_CREATE)

###############################################################################
# test_config_destroy_config_table
###############################################################################

DESTROY_TARGET = test_config_destroy_config_table

TEST_DESTROY = $(TEST_SRC_DIR)/$(DESTROY_TARGET).c

BIN_DESTROY = $(BIN_DIR)/$(DESTROY_TARGET)

$(DESTROY_TARGET): $(BIN_DESTROY)
	@echo "[OK] Built $@ => $<"

$(BIN_DESTROY): $(TEST_DESTROY) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_DESTROY)"
	$(CC) $(CFLAGS) $(PROXY_INC) $(UNITY_INC) -o $@ $(TEST_DESTROY) $(UNITY_SRC) $(LDFLAGS_CONFIG)

clean_$(DESTROY_TARGET):
	rm -rf $(BIN_DESTROY)

###############################################################################
# Auxiliary
###############################################################################

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all \
		$(CREATE_TARGET) \
		$(DESTROY_TARGET) \
		clean_$(CREATE_TARGET) \
		clean_$(DESTROY_TARGET)

all: $(CREATE_TARGET) \
	 $(DESTROY_TARGET)
