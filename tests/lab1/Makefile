# tests/lab1/Makefile

###############################################################################
# Makefile for lab1
# Builds all tests (config, logger, plugins) using Unity.
###############################################################################

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)/../../../proxy_anton

UNITY_INC  := -I../common/unity
UNITY_SRC  := ../common/unity/unity.c
COMMON_INC := -I${PROXY_DIR}/src/include

CFLAGS := $(CFLAGS) $(UNITY_INC) $(COMMON_INC)

BIN_DIR := bin

LDFLAGS_CONFIG  := -L$(PROXY_DIR)/install -lconfig
LDFLAGS_LOGGER  := -L$(PROXY_DIR)/install -llogger -Wl,-rpath,$(PROXY_DIR)/install
LDFLAGS_PLUGIN_GREETING  := -ldl -Wl,-rpath,$(PROXY_DIR)/install/plugins -rdynamic

DIR_CONFIG  := config
DIR_LOGGER  := logger
DIR_PLUGIN_GREETING  := plugins/greeting

SRC_CONFIG          := $(DIR_CONFIG)/c_tests
SRC_LOGGER          := $(DIR_LOGGER)/c_tests
SRC_PLUGIN_GREETING := $(DIR_PLUGIN_GREETING)/c_tests

SRCS_CONFIG := $(wildcard $(SRC_CONFIG)/*.c)
SRCS_LOGGER := $(wildcard $(SRC_LOGGER)/*.c)
SRCS_PLUGIN_GREETING := $(wildcard $(SRC_PLUGIN_GREETING)/*.c)

BINS_CONFIG := $(patsubst $(SRC_CONFIG)/%.c, $(BIN_DIR)/%, $(SRCS_CONFIG))
BINS_LOGGER := $(patsubst $(SRC_LOGGER)/%.c, $(BIN_DIR)/%, $(SRCS_LOGGER))
BINS_PLUGIN_GREETING := $(patsubst $(SRC_PLUGIN_GREETING)/%.c, $(BIN_DIR)/%, $(SRCS_PLUGIN_GREETING))

###############################################################################
# Build targets
###############################################################################

.PHONY: all config logger plugin_greeting

all: config logger plugin_greeting

config: $(BINS_CONFIG)
	@echo "Config tests built."

logger: stubs_time $(BINS_LOGGER)
	@echo "Logger tests built."

plugin_greeting: $(BINS_PLUGIN_GREETING)
	@echo "Plugin_greeting tests built"

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

clean:
	@echo "Cleaning binaries..."
	@rm -rf $(BIN_DIR)

###############################################################################
# Rules making Config tests
###############################################################################

$(BIN_DIR)/%: $(SRC_CONFIG)/%.c | $(BIN_DIR)
	@echo "Building config test: $@ from $< ..."
	$(CC) $(CFLAGS) $(UNITY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_CONFIG)

###############################################################################
# Build stubs for modules
###############################################################################

# --- Time stubs (compatibility) ---
# The time stub is located in tests/stubs/time/good
TIME_STUB_SRC := ../stubs/time/good/time_stub.c
TIME_STUB_LIB := $(BIN_DIR)/libtime_stub.a

$(TIME_STUB_LIB): $(TIME_STUB_SRC) | $(BIN_DIR)
	@echo "Building time stub library: $@"
	$(CC) $(CFLAGS) -c $< -o $(BIN_DIR)/time_stub.o
	ar rcs $@ $(BIN_DIR)/time_stub.o

.PHONY: stubs_time
stubs_time: $(TIME_STUB_LIB)
	@echo "Time stub built."

# --- Logger stubs (bad) ---
# Stubs for the logger that simulate errors are located in tests/stubs/logger/bad
STUBS_LOGGER_BAD_DIR := ../stubs/logger/bad
STUBS_LOGGER_BAD_SRC := $(wildcard $(STUBS_LOGGER_BAD_DIR)/*.c)
STUBS_LOGGER_BAD_SO := $(addprefix $(BIN_DIR)/, $(notdir $(STUBS_LOGGER_BAD_SRC:.c=.so)))


.PHONY: stubs_logger_bad
stubs_logger_bad: $(STUBS_LOGGER_BAD_SO)
	@echo "Logger bad stubs built."

$(STUBS_LOGGER_BAD_SO): $(BIN_DIR)/%.so : $(STUBS_LOGGER_BAD_DIR)/%.c | $(BIN_DIR)
	@echo "Building logger bad stub: $@ from $< ..."
	$(CC) -shared -fPIC $(CFLAGS) -o $@ $<

# --- Plugin stubs (bad) ---
# Stubs for plugins (e.g., greeting) that simulate errors are located in tests/stubs/plugin/greeting/bad
STUBS_PLUGIN_BAD_DIR := ../stubs/plugin/greeting/bad
STUBS_PLUGIN_BAD_SRC := $(wildcard $(STUBS_PLUGIN_BAD_DIR)/*.c)
STUBS_PLUGIN_BAD_SO := $(addprefix $(BIN_DIR)/, $(notdir $(STUBS_PLUGIN_BAD_SRC:.c=.so)))

.PHONY: stubs_plugin_bad
stubs_plugin_bad: $(STUBS_PLUGIN_BAD_SO)
	@echo "Plugin bad stubs built."

$(STUBS_PLUGIN_BAD_SO): $(BIN_DIR)/%.so : $(STUBS_PLUGIN_BAD_DIR)/%.c | $(BIN_DIR)
	@echo "Building plugin bad stub: $@ from $< ..."
	$(CC) -shared -fPIC $(CFLAGS) -o $@ $< $(LDFLAGS_PLUGIN_GREETING)

.PHONY: all_stubs
all_stubs: stubs_time stubs_logger_bad stubs_plugin_bad
	@echo "All stubs built."