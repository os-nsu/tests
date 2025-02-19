# tests/lab2/Makefile

###############################################################################
# Makefile for lab1
# Builds all tests (config, logger, plugins) using Unity.
###############################################################################

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)/../../../proxy_anton
INSTALL_DIR = ${PROXY_DIR}/install

UNITY_INC  := -I../common/unity
UNITY_SRC  := ../common/unity/unity.c
COMMON_INC := -I${PROXY_DIR}/src/include

CFLAGS := $(CFLAGS) $(UNITY_INC) $(COMMON_INC)

BIN_DIR := bin

LDFLAGS_CONFIG  := -L$(INSTALL_DIR) -lconfig
LDFLAGS_LOGGER  := -L$(INSTALL_DIR) -llogger -Wl,-rpath,$(INSTALL_DIR)
LDFLAGS_TIME  := -L$(INSTALL_DIR) -ltime -Wl,-rpath,$(INSTALL_DIR)

DIR_CONFIG  := config
DIR_LOGGER  := logger
DIR_TIME := time

SRC_CONFIG          := $(DIR_CONFIG)/c_tests
SRC_LOGGER          := $(DIR_LOGGER)/c_tests
SRC_TIME := $(DIR_TIME)/c_tests

SRCS_CONFIG := $(wildcard $(SRC_CONFIG)/*.c)
SRCS_LOGGER := $(wildcard $(SRC_LOGGER)/*.c)
SRCS_TIME := $(wildcard $(SRC_TIME)/*.c)

BINS_CONFIG := $(patsubst $(SRC_CONFIG)/%.c, $(BIN_DIR)/%, $(SRCS_CONFIG))
BINS_LOGGER := $(patsubst $(SRC_LOGGER)/%.c, $(BIN_DIR)/%, $(SRCS_LOGGER))
BINS_TIME := $(patsubst $(SRC_TIME)/%.c, $(BIN_DIR)/%, $(SRCS_TIME))

###############################################################################
# Build targets
###############################################################################

.PHONY: all config logger clean

all: time

config: $(BINS_CONFIG)
	@echo "Config tests built."

logger: $(BINS_LOGGER)
	@echo "Logger tests built."

time: $(BINS_TIME)
	@echo "Time tests built."

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
# Rules making Logger tests
###############################################################################


$(BIN_DIR)/%: $(SRC_LOGGER)/%.c | $(BIN_DIR)
	@echo "Building logger test: $@ from $< ..."
	$(CC) $(CFLAGS) $(UNITY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_LOGGER)

###############################################################################
# Rules making my_time tests
###############################################################################

$(BIN_DIR)/%: $(SRC_TIME)/%.c | $(BIN_DIR)
	@echo "Building time test: $@ from $< ..."
	$(CC) $(CFLAGS) $(UNITY_INC) -o $@ $< $(UNITY_SRC) $(LDFLAGS_TIME)

###############################################################################
# Build stubs
###############################################################################

DIR_LOGGER_STUBS          := $(DIR_LOGGER)/stubs
STUBS_LOGGER_SRC := $(wildcard $(DIR_LOGGER_STUBS)/*.c)
STUBS_LOGGER_SO  := $(patsubst $(DIR_LOGGER_STUBS)/%.c, $(BIN_DIR)/%.so, $(STUBS_LOGGER_SRC))

.PHONY: stubs_logger
stubs_logger: $(STUBS_LOGGER_SO)
	@echo "Logger stubs built."

$(BIN_DIR)/%.so: $(DIR_LOGGER_STUBS)/%.c | $(BIN_DIR)
	@echo "Building logger stub: $@ from $< ..."
	$(CC) -shared -fPIC $(CFLAGS) -o $@ $<


