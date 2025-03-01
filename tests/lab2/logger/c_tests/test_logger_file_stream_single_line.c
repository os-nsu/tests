// tests/lab2/logger/c_tests/test_logger_file_stream_single_line.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "logger.h"

char *LOG_FILENAME = "single_line.log";

void setUp(void) {
    int ret = init_logger(LOG_FILENAME, 1024);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "init_logger() should return 0 on first call");
}

void tearDown(void) {
    int ret = fini_logger();
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "fini_logger() should return 0 if not yet freed");
}

void test_write_single_line(void) {
    int return_value = write_log(FILESTREAM, LOG_INFO, __FILE__, __LINE__,
                         "Hello from single_line test: %d", 123);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, return_value, "write_log() must return 0 on success");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_write_single_line);
    return UNITY_END();
}
