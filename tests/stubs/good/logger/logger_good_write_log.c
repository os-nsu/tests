// tests/stubs/bad/logger_bad_write_log.c

#include "logger.h"

int write_log(OutputStream stream, LogLevel level,
              char *filename, int line_number, char *format, ...)
{
    return 0;
}
