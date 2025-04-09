# tests/lab1/master/Makefile

CC        ?= gcc
CFLAGS    ?= -Og -fno-omit-frame-pointer -ggdb3 -Werror -Wall

PROXY_DIR ?= $(shell pwd)
PROXY_INC ?= -I$(PROXY_DIR)/src/include

BIN_DIR   ?= bin

LAB_NUMBER ?= 1

STUBS_DIR ?= $(shell pwd)/../../stubs

STUBS_GOOD_LOGGER := $(STUBS_DIR)/good/logger
STUBS_BAD_LOGGER  := $(STUBS_DIR)/bad/logger

STUBS_GOOD_PLUGIN_GREETING := $(STUBS_DIR)/good/plugins/greeting
STUBS_BAD_PLUGIN_GREETING := $(STUBS_DIR)/bad/plugins/greeting

###############################################################################
# logger_bad_init.so
###############################################################################

LOGGER_BAD_INIT_TARGET = logger_bad_init
LOGGER_BAD_INIT_BIN = $(BIN_DIR)/logger_bad_init.so

$(LOGGER_BAD_INIT_TARGET): $(LOGGER_BAD_INIT_BIN)
	@echo "[OK] Built $@ => $<"

logger_bad_init_SOURCES := $(STUBS_BAD_LOGGER)/$(LOGGER_BAD_INIT_TARGET).c \
								$(STUBS_GOOD_LOGGER)/logger_good_fini.c

ifeq ($(LAB_NUMBER),2)
logger_bad_init_SOURCES := $(logger_bad_init_SOURCES) \
						   $(STUBS_GOOD_LOGGER)/logger_good_write_log.c
endif

$(LOGGER_BAD_INIT_BIN): $(logger_bad_init_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^ (LAB_NUMBER=$(LAB_NUMBER))"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(LOGGER_BAD_INIT_TARGET):
	rm -rf $(LOGGER_BAD_INIT_BIN)

###############################################################################
# logger_bad_fini.so
###############################################################################

LOGGER_BAD_FINI_TARGET = logger_bad_fini
LOGGER_BAD_FINI_BIN = $(BIN_DIR)/$(LOGGER_BAD_FINI_TARGET).so

$(LOGGER_BAD_FINI_TARGET): $(LOGGER_BAD_FINI_BIN)
	@echo "[OK] Built $@ => $<"

logger_bad_fini_SOURCES := $(STUBS_GOOD_LOGGER)/logger_good_init.c \
										  $(STUBS_BAD_LOGGER)/$(LOGGER_BAD_FINI_TARGET).c

ifeq ($(LAB_NUMBER),2)
logger_bad_fini_SOURCES := $(logger_bad_fini_SOURCES) \
						   $(STUBS_GOOD_LOGGER)/logger_good_write_log.c
endif

$(LOGGER_BAD_FINI_BIN): $(logger_bad_fini_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^ (LAB_NUMBER=$(LAB_NUMBER))"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(LOGGER_BAD_FINI_TARGET):
	rm -rf $(LOGGER_BAD_FINI_BIN)

###############################################################################
# greeting_bad_init.so
###############################################################################

GREETING_BAD_INIT_TARGET = greeting_bad_init
GREETING_BAD_INIT_BIN = $(BIN_DIR)/$(GREETING_BAD_INIT_TARGET).so

$(GREETING_BAD_INIT_TARGET): $(GREETING_BAD_INIT_BIN)
	@echo "[OK] Built $@ => $<"

greeting_bad_init_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_name.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_fini.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(GREETING_BAD_INIT_BIN): $(greeting_bad_init_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(GREETING_BAD_INIT_TARGET):
	rm -rf $(GREETING_BAD_INIT_BIN)

###############################################################################
# greeting_bad_name.so
###############################################################################

GREETING_BAD_NAME_TARGET = greeting_bad_name
GREETING_BAD_NAME_BIN = $(BIN_DIR)/$(GREETING_BAD_NAME_TARGET).so

$(GREETING_BAD_NAME_TARGET): $(GREETING_BAD_NAME_BIN)
	@echo "[OK] Built $@ => $<"

greeting_bad_name_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_init.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_fini.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(GREETING_BAD_NAME_BIN): $(greeting_bad_name_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(GREETING_BAD_NAME_TARGET):
	rm -rf $(GREETING_BAD_NAME_BIN)

###############################################################################
# greeting_bad_fini.so
###############################################################################

GREETING_BAD_FINI_TARGET = greeting_bad_fini
GREETING_BAD_FINI_BIN = $(BIN_DIR)/$(GREETING_BAD_FINI_TARGET).so

$(GREETING_BAD_FINI_TARGET): $(GREETING_BAD_FINI_BIN)
	@echo "[OK] Built $@ => $<"

greeting_bad_fini_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_init.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_name.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_hook.c

$(GREETING_BAD_FINI_BIN): $(greeting_bad_fini_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(GREETING_BAD_FINI_TARGET):
	rm -rf $(GREETING_BAD_FINI_BIN)

###############################################################################
# greeting_bad_hook.so
###############################################################################

GREETING_BAD_HOOK_TARGET = greeting_bad_hook
GREETING_BAD_HOOK_BIN = $(BIN_DIR)/$(GREETING_BAD_HOOK_TARGET).so

$(GREETING_BAD_HOOK_TARGET): $(GREETING_BAD_HOOK_BIN)
	@echo "[OK] Built $@ => $<"

greeting_bad_hook_SOURCES := $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_init.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_name.c \
										  $(STUBS_GOOD_PLUGIN_GREETING)/greeting_good_fini.c

$(BIGREETING_BAD_HOOK_BINN_DIR): $(greeting_bad_hook_SOURCES) | $(BIN_DIR)
	@echo "Building mosaic $@ from $^"
	$(CC) -shared -fPIC $(CFLAGS) $(PROXY_INC) -o $@ $^

clean_$(GREETING_BAD_HOOK_TARGET):
	rm -rf $(BIGREETING_BAD_HOOK_BINN_DIR)

###############################################################################
# Auxiliary
###############################################################################

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all \
		$(LOGGER_BAD_INIT_TARGET) \
		$(LOGGER_BAD_FINI_TARGET) \
		$(GREETING_BAD_INIT_TARGET) \
		$(GREETING_BAD_NAME_TARGET) \
		$(GREETING_BAD_FINI_TARGET) \
		$(GREETING_BAD_HOOK_TARGET) \
		clean_$(LOGGER_BAD_INIT_TARGET) \
		clean_$(GREETING_BAD_INIT_TARGET) \
		clean_$(GREETING_BAD_NAME_TARGET) \
		clean_$(GREETING_BAD_FINI_TARGET) \
		clean_$(ARGSGREETING_BAD_HOOK_TARGET_TARGET)

all: $(LOGGER_BAD_INIT_TARGET) \
	 $(LOGGER_BAD_FINI_TARGET) \
	 $(GREETING_BAD_INIT_TARGET) \
	 $(GREETING_BAD_NAME_TARGET) \
	 $(GREETING_BAD_FINI_TARGET) \
	 $(GREETING_BAD_HOOK_TARGET)
