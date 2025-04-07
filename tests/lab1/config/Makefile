# File: tests/lab1/config/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

# Proxy
PROXY_DIR ?= $(shell pwd)/../../../../proxy_anton
PROXY_INC := -I$(PROXY_DIR)/src/include

# Unity
UNITY_DIR  := ../../common/unity
UNITY_INC  := -I$(UNITY_DIR)
UNITY_SRC  := $(UNITY_DIR)/unity.c

# Где взять libconfig.a
LDFLAGS_CONFIG := -L$(PROXY_DIR)/install -lconfig

# Where your test .c sources are
TEST_SRC_DIR  := c_tests

# Where to place compiled test binaries
BIN_DIR := bin

# Исходники тестов
TEST_C_CREATE  = $(TEST_SRC_DIR)/test_config_create_config_table.c
TEST_C_DESTROY = $(TEST_SRC_DIR)/test_config_destroy_config_table.c

.PHONY: all clean \
        test_config_create_config_table test_config_destroy_config_table

all: test_config_create_config_table test_config_destroy_config_table

###############################################################################
# test_config_create_config_table
###############################################################################

TEST_CREATE  = $(TEST_SRC_DIR)/test_config_create_config_table.c

BIN_CREATE  = $(BIN_DIR)/test_config_create_config_table

test_config_create_config_table: $(BIN_CREATE)
	@echo "[OK] Built $@ => $<"

$(BIN_CREATE): $(TEST_C_CREATE) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_CREATE)"
	$(CC) $(CFLAGS) $(PROXY_INC) $(UNITY_INC) -o $@ $(TEST_CREATE) $(UNITY_SRC) $(LDFLAGS_CONFIG)

###############################################################################
# test_config_destroy_config_table
###############################################################################

TEST_DESTROY = $(TEST_SRC_DIR)/test_config_destroy_config_table.c

BIN_DESTROY = $(BIN_DIR)/test_config_destroy_config_table

test_config_destroy_config_table: $(BIN_DESTROY)
	@echo "[OK] Built $@ => $<"

$(BIN_DESTROY): $(TEST_C_DESTROY) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_DESTROY)"
	$(CC) $(CFLAGS) $(PROXY_INC) $(UNITY_INC) -o $@ $(TEST_DESTROY) $(UNITY_SRC) $(LDFLAGS_CONFIG)

###############################################################################
# helpers
###############################################################################

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	@echo "Cleaning config test binaries..."
	rm -rf $(BIN_DIR)
