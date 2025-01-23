# lab1/logger/Makefile

MAINDIR ?= $(shell pwd)

CC = gcc
LDFLAGS = -L$(PROXY_DIR)/install -llogger

SRCS = $(wildcard *.c)

TARGET = test_logger

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(COPT) $(CFLAGS) -o $(TARGET) $(SRCS) $(LDFLAGS)

clean:
	rm -f $(TARGET)
