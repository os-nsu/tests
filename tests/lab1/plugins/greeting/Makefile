# tests/lab1/plugins/greeting/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)
PROXY_INC := -I$(PROXY_DIR)/src/include

UNITY_DIR  := ../../../common/unity
UNITY_INC  := -I$(UNITY_DIR)
UNITY_SRC  := $(UNITY_DIR)/unity.c

LDFLAGS_PLUGIN = -ldl -Wl,-rpath,$(PROXY_DIR)/install/plugins -rdynamic

BIN_DIR := bin

TEST_SRC_DIR  := c_tests

###############################################################################
# 1) Unity-test targets
###############################################################################

###############################################################################
# Цель test_plugin_greeting_dlopen
###############################################################################

DLOPEN_TARGET = test_plugin_greeting_dlopen
BIN_DLOPEN := $(BIN_DIR)/$(DLOPEN_TARGET)
TEST_C_DLOPEN := c_tests/$(DLOPEN_TARGET).c

$(DLOPEN_TARGET): $(BIN_DLOPEN)
	@echo "[OK] Built $@ => $<"

$(BIN_DLOPEN): $(TEST_C_DLOPEN) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(DLOPEN_TARGET):
	rm -rf $(BIN_DLOPEN)

###############################################################################
# Цель test_plugin_greeting_dlsym_init
###############################################################################

DLSYM_INIT_TARGET = test_plugin_greeting_dlsym_init
BIN_DLSYM_INIT := $(BIN_DIR)/$(DLSYM_INIT_TARGET)
TEST_C_DLSYM_INIT := $(TEST_SRC_DIR)/$(DLSYM_INIT_TARGET).c

$(DLSYM_INIT_TARGET): $(BIN_DLSYM_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_INIT): $(TEST_C_DLSYM_INIT) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(DLSYM_INIT_TARGET):
	rm -rf $(BIN_DLSYM_INIT)

###############################################################################
# Цель test_plugin_greeting_dlsym_name
###############################################################################

DLSYM_NAME_TARGET = test_plugin_greeting_dlsym_name
BIN_DLSYM_NAME := $(BIN_DIR)/$(DLSYM_NAME_TARGET)
TEST_C_DLSYM_NAME := $(TEST_SRC_DIR)/$(DLSYM_NAME_TARGET).c

$(DLSYM_NAME_TARGET): $(BIN_DLSYM_NAME)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_NAME): $(TEST_C_DLSYM_NAME) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(DLSYM_NAME_TARGET):
	rm -rf $(BIN_DLSYM_NAME)

###############################################################################
# Цель test_plugin_greeting_dlsym_fini
###############################################################################

DLSYM_FINI_TARGET = test_plugin_greeting_dlsym_fini
BIN_DLSYM_FINI := $(BIN_DIR)/$(DLSYM_FINI_TARGET)
TEST_C_DLSYM_FINI := $(TEST_SRC_DIR)/$(DLSYM_FINI_TARGET).c

$(DLSYM_FINI_TARGET): $(BIN_DLSYM_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_DLSYM_FINI): $(TEST_C_DLSYM_FINI) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(DLSYM_FINI_TARGET):
	rm -rf $(BIN_DLSYM_FINI)

###############################################################################
# Цель test_plugin_greeting_call_init
###############################################################################

CALL_INIT_TARGET = test_plugin_greeting_call_init
BIN_CALL_INIT := $(BIN_DIR)/$(CALL_INIT_TARGET)
TEST_C_CALL_INIT := $(TEST_SRC_DIR)/$(CALL_INIT_TARGET).c

$(CALL_INIT_TARGET): $(BIN_CALL_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_INIT): $(TEST_C_CALL_INIT) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(CALL_INIT_TARGET):
	rm -rf $(BIN_CALL_INIT)

###############################################################################
# Цель test_plugin_greeting_call_name
###############################################################################

CALL_NAME_TARGET = test_plugin_greeting_call_name
BIN_CALL_NAME := $(BIN_DIR)/$(CALL_NAME_TARGET)
TEST_C_CALL_NAME := $(TEST_SRC_DIR)/$(CALL_NAME_TARGET).c

$(CALL_NAME_TARGET): $(BIN_CALL_NAME)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_NAME): $(TEST_C_CALL_NAME) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(CALL_NAME_TARGET):
	rm -rf $(BIN_CALL_NAME)

###############################################################################
# Цель test_plugin_greeting_call_fini
###############################################################################

CALL_FINI_TARGET = test_plugin_greeting_call_fini
BIN_CALL_FINI := $(BIN_DIR)/$(CALL_FINI_TARGET)
TEST_C_CALL_FINI := $(TEST_SRC_DIR)/$(CALL_FINI_TARGET).c

$(CALL_FINI_TARGET): $(BIN_CALL_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_CALL_FINI): $(TEST_C_CALL_FINI) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(CALL_FINI_TARGET):
	rm -rf $(BIN_CALL_FINI)

###############################################################################
# Цель test_plugin_greeting_dlclose
###############################################################################

DLCLOSE_TARGET = test_plugin_greeting_dlclose
BIN_DLCLOSE := $(BIN_DIR)/$(DLCLOSE_TARGET)
TEST_C_DLCLOSE := $(TEST_SRC_DIR)/$(DLCLOSE_TARGET).c

$(DLCLOSE_TARGET): $(BIN_DLCLOSE)
	@echo "[OK] Built $@ => $<"

$(BIN_DLCLOSE): $(TEST_C_DLCLOSE) | $(BIN_DIR)
	@echo "Building $@ from $<"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_PLUGIN)

clean_$(DLCLOSE_TARGET):
	rm -rf $(BIN_DLCLOSE)

###############################################################################
# Auxiliary
###############################################################################

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

.PHONY: all \
		$(DLOPEN_TARGET) \
		$(DLSYM_INIT_TARGET) \
		$(DLSYM_NAME_TARGET) \
		$(DLSYM_FINI_TARGET) \
		$(CALL_INIT_TARGET) \
		$(CALL_NAME_TARGET) \
		$(CALL_FINI_TARGET) \
		$(DLCLOSE_TARGET) \
		clean_$(DLOPEN_TARGET) \
		clean_$(DLSYM_INIT_TARGET) \
		clean_$(DLSYM_NAME_TARGET) \
		clean_$(DLSYM_FINI_TARGET) \
		clean_$(CALL_INIT_TARGET) \
		clean_$(CALL_NAME_TARGET) \
		clean_$(CALL_FINI_TARGET) \
		clean_$(DLCLOSE_TARGET)

all: $(DLOPEN_TARGET) \
	 $(DLSYM_INIT_TARGET) \
	 $(DLSYM_NAME_TARGET) \
	 $(DLSYM_FINI_TARGET) \
	 $(CALL_INIT_TARGET) \
	 $(CALL_NAME_TARGET) \
	 $(CALL_FINI_TARGET) \
	 $(DLCLOSE_TARGET)
