# tests/lab1/plugins/greeting/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)/../../../../../proxy_anton
PROXY_INC := -I$(PROXY_DIR)/src/include

UNITY_DIR  := ../../../common/unity
UNITY_INC  := -I$(UNITY_DIR)
UNITY_SRC  := $(UNITY_DIR)/unity.c

LDFLAGS_PLUGIN = -ldl -Wl,-rpath,$(PROXY_DIR)/install/plugins -rdynamic

BIN_DIR := bin

TEST_C_DLOPEN       := c_tests/test_plugin_greeting_dlopen.c
TEST_C_DLSYM_INIT   := c_tests/test_plugin_greeting_dlsym_init.c
TEST_C_DLSYM_NAME   := c_tests/test_plugin_greeting_dlsym_name.c
TEST_C_DLSYM_FINI   := c_tests/test_plugin_greeting_dlsym_fini.c
TEST_C_CALL_INIT    := c_tests/test_plugin_greeting_call_init.c
TEST_C_CALL_NAME    := c_tests/test_plugin_greeting_call_name.c
TEST_C_CALL_FINI    := c_tests/test_plugin_greeting_call_fini.c
TEST_C_DLCLOSE      := c_tests/test_plugin_greeting_dlclose.c

BIN_DLOPEN       := $(BIN_DIR)/test_plugin_greeting_dlopen
BIN_DLSYM_INIT   := $(BIN_DIR)/test_plugin_greeting_dlsym_init
BIN_DLSYM_NAME   := $(BIN_DIR)/test_plugin_greeting_dlsym_name
BIN_DLSYM_FINI   := $(BIN_DIR)/test_plugin_greeting_dlsym_fini
BIN_CALL_INIT    := $(BIN_DIR)/test_plugin_greeting_call_init
BIN_CALL_NAME    := $(BIN_DIR)/test_plugin_greeting_call_name
BIN_CALL_FINI    := $(BIN_DIR)/test_plugin_greeting_call_fini
BIN_DLCLOSE      := $(BIN_DIR)/test_plugin_greeting_dlclose


.PHONY: all clean \
        test_plugin_greeting_dlopen \
        test_plugin_greeting_dlsym_init \
        test_plugin_greeting_dlsym_name \
        test_plugin_greeting_dlsym_fini \
        test_plugin_greeting_call_init \
        test_plugin_greeting_call_name \
        test_plugin_greeting_call_fini \
        test_plugin_greeting_dlclose

all: test_plugin_greeting_dlopen test_plugin_greeting_dlsym_init \
     test_plugin_greeting_dlsym_name test_plugin_greeting_dlsym_fini \
     test_plugin_greeting_call_init test_plugin_greeting_call_name \
     test_plugin_greeting_call_fini test_plugin_greeting_dlclose

###############################################################################
# 1) Unity-test targets
###############################################################################

###############################################################################
# Цель test_plugin_greeting_dlopen
###############################################################################
test_plugin_greeting_dlopen: $(BIN_DLOPEN)
	@echo "[OK] Built $@ => $<"

$(BIN_DLOPEN): $(TEST_C_DLOPEN) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_dlsym_init
###############################################################################
test_plugin_greeting_dlsym_init: $(BIN_DLSYM_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_INIT): $(TEST_C_DLSYM_INIT) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_dlsym_name
###############################################################################
test_plugin_greeting_dlsym_name: $(BIN_DLSYM_NAME)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_NAME): $(TEST_C_DLSYM_NAME) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_dlsym_fini
###############################################################################
test_plugin_greeting_dlsym_fini: $(BIN_DLSYM_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_FINI): $(TEST_C_DLSYM_FINI) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_call_init
###############################################################################
test_plugin_greeting_call_init: $(BIN_CALL_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_INIT): $(TEST_C_CALL_INIT) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_call_name
###############################################################################
test_plugin_greeting_call_name: $(BIN_CALL_NAME)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_NAME): $(TEST_C_CALL_NAME) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_call_fini
###############################################################################
test_plugin_greeting_call_fini: $(BIN_CALL_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_FINI): $(TEST_C_CALL_FINI) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


###############################################################################
# Цель test_plugin_greeting_dlclose
###############################################################################
test_plugin_greeting_dlclose: $(BIN_DLCLOSE)
	@echo "[OK] Built $@ => $<"

$(BIN_DLCLOSE): $(TEST_C_DLCLOSE) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)


$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

clean:
	@echo "Cleaning greeting plugin tests..."
	rm -rf $(BIN_DIR)