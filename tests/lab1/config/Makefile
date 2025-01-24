# tests/lab1/config/Makefile

MAINDIR ?= $(shell pwd)

CC = gcc
LDFLAGS = -L$(PROXY_DIR)/install -lconfig

SRCS = $(wildcard *.c)

TARGET = test_config

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(COPT) $(CFLAGS) -o $(TARGET) $(SRCS) $(LDFLAGS)

clean:
	rm -f $(TARGET)
