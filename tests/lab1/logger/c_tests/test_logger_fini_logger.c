//tests/lab1/logger/c_tests/test_logger_fini_logger.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "logger.h"

void setUp(void) {
    init_logger(NULL, -1);
}

void tearDown(void) {
    init_logger(NULL, -1);
}

// Test 1: The first cleanup should return 0
void test_fini_logger_first_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, fini_logger(), "The first call to fini_logger() should return 0!");
}

// Test 2: A repeated cleanup should return 1
void test_fini_logger_second_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, fini_logger(), "The first call to fini_logger() should return 0!");
    TEST_ASSERT_EQUAL_INT_MESSAGE(1, fini_logger(), "A repeated call to fini_logger() should return 1!");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_fini_logger_first_call);
    RUN_TEST(test_fini_logger_second_call);
    return UNITY_END();
}
