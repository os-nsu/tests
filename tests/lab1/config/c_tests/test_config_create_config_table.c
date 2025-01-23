// tests/lab1/config/c_tests/test_config_create_config_table.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "config.h"

void setUp(void) {
}

void tearDown(void) {
}

// Test 1: The first initialization should return 0
void test_create_config_first_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, create_config_table(),  "The first call to create_config_table() should return 0!");
}

// Test 2: A repeated call should return -1
void test_create_config_second_call(void) {
    create_config_table();
    TEST_ASSERT_EQUAL_INT_MESSAGE(1, create_config_table(), "A repeated call to create_config_table() should return 1!");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_create_config_first_call);
    RUN_TEST(test_create_config_second_call);
    return UNITY_END();
}
