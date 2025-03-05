// tests/stubs/logger/logger_bad_fini.c

#include "../../src/include/logger.h"

int init_logger(char *path, int file_size_limit) {
    return 0;
}

int write_log(enum OutputStream stream, enum LogLevel level, const char *filename, int line_number, const char *format, ...) {
    return 0;
}

int fini_logger(void) {
    return 1;
}
