//tests/lab1/logger/c_tests/test_logger_init_logger.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "logger.h"

void setUp(void) {
}

void tearDown(void) {
}

// Test 1: The first initialization should return 0
void test_init_logger_first_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, init_logger(NULL, -1), "The first call to init_logger() should return 0!");
}

// Test 2: A repeated call should return 1
void test_init_logger_second_call(void) {
    init_logger(NULL, -1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(1, init_logger(NULL, -1), "A repeated call to init_logger() should return 1!");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_init_logger_first_call);
    RUN_TEST(test_init_logger_second_call);
    return UNITY_END();
}
