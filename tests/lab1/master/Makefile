# tests/lab1/master/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)/../../../../proxy_anton
PROXY_INC ?= -I$(PROXY_DIR)/src/include

BIN_DIR   ?= bin

LAB_NUMBER ?= 1

STUBS_DIR ?= $(shell pwd)/../../stubs

STUBS_GOOD_LOGGER := $(STUBS_DIR)/good/logger
STUBS_BAD_LOGGER  := $(STUBS_DIR)/bad/logger

STUBS_GOOD_PLUGIN_GREETING := $(STUBS_DIR)/good/plugins/greeting
STUBS_BAD_PLUGIN_GREETING := $(STUBS_DIR)/bad/plugins/greeting

.PHONY: all clean \
        logger_bad_fini logger_bad_init

all: logger_bad_fini logger_bad_init
	@echo "[master] Built all mosaic stubs"

###############################################################################
# logger_bad_init.so
###############################################################################

logger_bad_init: $(BIN_DIR)/logger_bad_init.so
	@echo "[OK] Built $@ => $<"

logger_bad_init_SOURCES := $(STUBS_BAD_LOGGER)/logger_bad_init.c \
                                $(STUBS_GOOD_LOGGER)/logger_good_fini.c

ifeq ($(LAB_NUMBER),2)
logger_bad_init_SOURCES := $(logger_bad_init_SOURCES) \
                           $(STUBS_GOOD_LOGGER)/logger_good_write_log.c
endif

$(BIN_DIR)/logger_bad_init.so: $(logger_bad_init_SOURCES)
	@mkdir -p $(BIN_DIR)
	@echo "Building mosaic $@ from $^ (LAB_NUMBER=$(LAB_NUMBER))"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

###############################################################################
# logger_bad_fini.so
###############################################################################

logger_bad_fini: $(BIN_DIR)/logger_bad_fini.so
	@echo "[OK] Built $@ => $<"

logger_bad_fini_SOURCES := $(STUBS_GOOD_LOGGER)/logger_good_init.c \
                                          $(STUBS_BAD_LOGGER)/logger_bad_fini.c

ifeq ($(LAB_NUMBER),2)
logger_bad_fini_SOURCES := $(logger_bad_fini_SOURCES) \
                           $(STUBS_GOOD_LOGGER)/logger_good_write_log.c
endif

$(BIN_DIR)/logger_bad_fini.so: $(logger_bad_fini_SOURCES)
	@mkdir -p $(BIN_DIR)
	@echo "Building mosaic $@ from $^ (LAB_NUMBER=$(LAB_NUMBER))"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

###############################################################################
# greeting_bad_init.so
###############################################################################

greeting_bad_init: $(BIN_DIR)/greeting_bad_init.so
	@echo "[OK] Built $@ => $<"

greeting_bad_init_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_name.c \
                                          $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_fini.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(BIN_DIR)/greeting_bad_init.so: $(greeting_bad_init_SOURCES)
	@mkdir -p $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

###############################################################################
# greeting_bad_name.so
###############################################################################

greeting_bad_name: $(BIN_DIR)/greeting_bad_name.so
	@echo "[OK] Built $@ => $<"

greeting_bad_name_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_init.c \
                                          $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_fini.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(BIN_DIR)/greeting_bad_name.so: $(greeting_bad_name_SOURCES)
	@mkdir -p $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

###############################################################################
# greeting_bad_fini.so
###############################################################################

greeting_bad_fini: $(BIN_DIR)/greeting_bad_fini.so
	@echo "[OK] Built $@ => $<"

greeting_bad_fini_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_init.c \
                                          $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_name.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(BIN_DIR)/greeting_bad_fini.so: $(greeting_bad_fini_SOURCES)
	@mkdir -p $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

###############################################################################
# helpers
###############################################################################

clean:
	@echo "[master] Cleaning mosaic stubs..."
	rm -rf $(BIN_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)
