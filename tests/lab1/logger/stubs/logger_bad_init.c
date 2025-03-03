//tests/lab1/logger/stubs/logger_bad_init.c

#include "../../src/include/logger.h"

int init_logger(char *path, int file_size_limit) {
    return 1;
}

int fini_logger(void) {
    return 0;
}
