//tests/lab2/logger/c_tests/test_logger_write_log_stdout.c

#include <stdio.h>
#include "unity.h"
#include "logger.h"

void setUp(void) {
    fini_logger();
}

void tearDown(void) {
    fini_logger();
}

void test_write_log_stdout(void) {
    int ret;

    ret = init_logger(NULL, 1024);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "init_logger() should return 0 with NULL path");

    ret = write_log(STDOUT, LOG_DEBUG, __FILE__, __LINE__, "STDOUT Debug message");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "STDOUT Debug log should return 0");

    ret = write_log(STDOUT, LOG_INFO, __FILE__, __LINE__, "STDOUT Info message");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "STDOUT Info log should return 0");

    ret = write_log(STDOUT, LOG_WARNING, __FILE__, __LINE__, "STDOUT Warning message");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "STDOUT Warning log should return 0");

    ret = write_log(STDOUT, LOG_ERROR, __FILE__, __LINE__, "STDOUT Error message");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "STDOUT Error log should return 0");

    ret = write_log(STDOUT, LOG_FATAL, __FILE__, __LINE__, "STDOUT Fatal message");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "STDOUT Fatal log should return 0");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_write_log_stdout);
    return UNITY_END();
}
