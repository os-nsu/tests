# tests/lab1/logger/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

# Proxy
PROXY_DIR ?= $(shell pwd)
PROXY_INC := -I${PROXY_DIR}/src/include

# Unity
UNITY_DIR  := ../../common/unity
UNITY_INC  := -I${UNITY_DIR}
UNITY_SRC  := $(UNITY_DIR)/unity.c

# Link with real logger
LDFLAGS_LOGGER := -L$(PROXY_DIR)/install -llogger -Wl,-rpath,$(PROXY_DIR)/install

# Where your test .c sources are
TEST_SRC_DIR  := c_tests

# Where to place compiled test binaries
BIN_DIR := bin

LAB_NUMBER ?= 1

STUBS_DIR ?= $(shell pwd)/../../stubs

STUBS_GOOD_DIR := $(STUBS_DIR)/good
STUBS_BAD_DIR  := $(STUBS_DIR)/bad

STUBS_GOOD_LOGGER := $(STUBS_DIR)/good/logger
STUBS_BAD_LOGGER  := $(STUBS_DIR)/bad/logger

###############################################################################
# Lab2
###############################################################################

STUBS_GOOD_TIME := $(STUBS_DIR)/good/time
STUBS_BAD_TIME  := $(STUBS_DIR)/bad/time

###############################################################################
# 1) Unity-test targets
###############################################################################

###############################################################################
# test_logger_init_logger
###############################################################################

INIT_TARGET = test_logger_init_logger

TEST_C_INIT = $(TEST_SRC_DIR)/$(INIT_TARGET).c
ifeq ($(LAB_NUMBER),2)
TEST_C_INIT += $(STUBS_GOOD_TIME)/time_good_get_time.c
endif

BIN_INIT = $(BIN_DIR)/$(INIT_TARGET)

$(INIT_TARGET): $(BIN_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_INIT): $(TEST_C_INIT) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_INIT)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_INIT) $(UNITY_SRC) $(LDFLAGS_LOGGER)

clean_$(INIT_TARGET):
	rm -rf $(BIN_INIT)

###############################################################################
# test_logger_fini_logger
###############################################################################

FINI_TARGET = test_logger_fini_logger

TEST_C_FINI = $(TEST_SRC_DIR)/$(FINI_TARGET).c
ifeq ($(LAB_NUMBER),2)
TEST_C_FINI += $(STUBS_GOOD_TIME)/time_good_get_time.c
endif

BIN_FINI = $(BIN_DIR)/$(FINI_TARGET)

$(FINI_TARGET): $(BIN_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_FINI): $(TEST_C_FINI) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_FINI)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_FINI) $(UNITY_SRC) $(LDFLAGS_LOGGER)

clean_$(FINI_TARGET):
	rm -rf $(BIN_FINI)

###############################################################################
# test_logger_init_logger_args
###############################################################################

ARGS_TARGET = test_logger_init_logger_args

TEST_C_ARGS = $(TEST_SRC_DIR)/$(ARGS_TARGET).c
ifeq ($(LAB_NUMBER),2)
TEST_C_ARGS += $(STUBS_GOOD_TIME)/time_good_get_time.c
endif

BIN_ARGS = $(BIN_DIR)/$(ARGS_TARGET)

$(ARGS_TARGET): $(BIN_ARGS)
	@echo "[OK] Built $@ => $<"

$(BIN_ARGS): $(TEST_C_ARGS) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_ARGS)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_ARGS) $(UNITY_SRC) $(LDFLAGS_LOGGER)

clean_$(ARGS_TARGET):
	rm -rf $(BIN_ARGS)

###############################################################################
# Auxiliary
###############################################################################

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all \
		$(INIT_TARGET) \
		$(FINI_TARGET) \
		$(ARGS_TARGET) \
		clean_$(INIT_TARGET) \
		clean_$(FINI_TARGET) \
		clean_$(ARGS_TARGET)

all: $(INIT_TARGET) \
	 $(FINI_TARGET) \
	 $(ARGS_TARGET)
