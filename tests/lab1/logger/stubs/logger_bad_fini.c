//tests/lab1/logger/stubs/logger_bad_fini.c

#include "../../src/include/logger.h"

int init_logger(char *path, int file_size_limit) {
    return 0;
}

int fini_logger(void) {
    return 1;
}
