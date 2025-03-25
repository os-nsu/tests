# tests/lab1/logger/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

# Proxy
PROXY_DIR ?= $(shell pwd)/../../../../proxy_anton
PROXY_INC := -I${PROXY_DIR}/src/include

# Unity
UNITY_DIR  := ../../common/unity
UNITY_INC  := -I${UNITY_DIR}
UNITY_SRC  := $(UNITY_DIR)/unity.c

# Link with real logger(а точно ли нам надо?)
LDFLAGS_LOGGER := -L$(PROXY_DIR)/install -llogger -Wl,-rpath,$(PROXY_DIR)/install

# Where your test .c sources are
TEST_SRC_DIR  := c_tests
TEST_C_INIT = $(TEST_SRC_DIR)/test_logger_init_logger.c
TEST_C_FINI = $(TEST_SRC_DIR)/test_logger_fini_logger.c
TEST_C_ARGS = $(TEST_SRC_DIR)/test_logger_init_logger_args.c

# Where to place compiled test binaries
BIN_DIR := bin
BIN_INIT = $(BIN_DIR)/test_logger_init_logger
BIN_FINI = $(BIN_DIR)/test_logger_fini_logger
BIN_ARGS = $(BIN_DIR)/test_logger_init_logger_args

STUBS_DIR ?= $(shell pwd)../../stubs
STUBS_GOOD_DIR := $(STUBS_DIR)/good
STUBS_BAD_DIR  := $(STUBS_DIR)/bad

# CFLAGS := $(CFLAGS) $(UNITY_INC) $(COMMON_INC)

.PHONY: all clean \
        test_logger_init_logger test_logger_fini_logger test_logger_init_logger_args

all: test_logger_init_logger test_logger_fini_logger test_logger_init_logger_args

###############################################################################
# 1) Unity-test targets
###############################################################################

###############################################################################
# test_logger_init_logger
###############################################################################

test_logger_init_logger: $(BIN_INIT)
	@echo "[OK] Built $@ => $<"

$(BIN_INIT): $(TEST_C_INIT) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_INIT)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_INIT) $(UNITY_SRC) $(LDFLAGS_LOGGER)

###############################################################################
# test_logger_fini_logger
###############################################################################

test_logger_fini_logger: $(BIN_FINI)
	@echo "[OK] Built $@ => $<"

$(BIN_FINI): $(TEST_C_FINI) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_FINI)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_FINI) $(UNITY_SRC) $(LDFLAGS_LOGGER)

###############################################################################
# test_logger_init_logger_args
###############################################################################

test_logger_init_logger_args: $(BIN_ARGS)
	@echo "[OK] Built $@ => $<"

$(BIN_ARGS): $(TEST_C_ARGS) | $(BIN_DIR)
	@echo "Building $@ from $(TEST_C_ARGS)"
	$(CC) $(CFLAGS) $(UNITY_INC) $(PROXY_INC) -o $@ $(TEST_C_ARGS) $(UNITY_SRC) $(LDFLAGS_LOGGER)

###############################################################################
# 2) Mosaic stubs: Build .so from multiple .c stubs (no .o)
###############################################################################

# stubs_mosaic: $(BIN_DIR)/logger_good_init_good_write_bad_fini.so
# 	@echo "Mosaic stubs built."

# $(BIN_DIR)/logger_bad_fini.so: \
#     $(STUBS_GOOD_DIR)/init.c \
#     $(STUBS_GOOD_DIR)/write.c \
#     $(STUBS_BAD_DIR)/fini.c | $(BIN_DIR)
# 	@echo "Linking $@"
# 	$(CC) -shared -fPIC $(CFLAGS) -I$(PROXY_DIR)/src/include \
# 	      -o $@ $^

# $(BIN_DIR)/logger_bad_fini.so: \
#     $(STUBS_GOOD_DIR)/init.c \
#     $(STUBS_GOOD_DIR)/write.c \
#     $(STUBS_BAD_DIR)/fini.c | $(BIN_DIR)
# 	@echo "Linking $@"
# 	$(CC) -shared -fPIC $(CFLAGS) -I$(PROXY_DIR)/src/include \
# 	      -o $@ $^

$(BIN_DIR):
	@mkdir -p $@

clean:
	@echo "Cleaning binaries in logger tests..."
	rm -rf $(BIN_DIR)