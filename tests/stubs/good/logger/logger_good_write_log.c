// tests/stubs/bad/logger_bad_write_log.c

#include "logger.h"

int write_log(enum OutputStream stream, enum LogLevel level,
              const char *filename, int line_number, const char *format, ...)
{
    return 0;
}
