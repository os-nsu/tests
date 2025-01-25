# tests/lab1/plugins/greeting/Makefile

MAINDIR ?= $(shell pwd)
CC = gcc

# Note:
# 1) -ldl, because we use dlopen.
# 2) -Wl,-rpath,$(PROXY_DIR)/install/plugins - ensures that "greeting.so" is searched in install/plugins
#    when we use dlopen("greeting.so") without the full path.
# 3) Most important: -rdynamic (or -Wl,-export-dynamic)
#    to make executor_start_hook visible as a global symbol.

LDFLAGS = -ldl -Wl,-rpath,$(PROXY_DIR)/install/plugins -rdynamic

SRCS = $(wildcard *.c)
TARGET = test_plugin_greeting

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(COPT) $(CFLAGS) -o $(TARGET) $(SRCS) $(LDFLAGS)

clean:
	rm -f $(TARGET)
