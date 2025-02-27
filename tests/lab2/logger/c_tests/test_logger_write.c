// tests/lab2/logger/c_tests/test_logger_file_stream.c
#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "logger.h"

static const char *TEST_LOG_FILENAME = "logger_file_stream.log";

void setUp(void) {
    int ret = init_logger(TEST_LOG_FILENAME, 1024 * 100);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "init_logger(...) must return 0 on first call");
}

void tearDown(void) {
    int ret = fini_logger();
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "fini_logger() must return 0 on first call");
}

void test_write_single_line(void) {
    write_log(FILESTREAM, LOG_INFO, __FILE__, __LINE__, "Hello from test_write_single_line");
    TEST_PASS();
}

void test_write_multiple_lines(void) {
    write_log(FILESTREAM, LOG_DEBUG, __FILE__, __LINE__, "First line");
    write_log(FILESTREAM, LOG_DEBUG, __FILE__, __LINE__, "Second line");
    TEST_PASS();
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_write_single_line);
    RUN_TEST(test_write_multiple_lines);
    return UNITY_END();
}
