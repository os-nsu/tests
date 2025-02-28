// tests/lab1/config/c_tests/test_config_destroy_config_table.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "config.h"

void setUp(void) {
    create_config_table();
}

void tearDown(void) {
    create_config_table();
}

// Test 1: The first cleanup should return 0
void test_destroy_config_table_first_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, destroy_config_table(), "The first call to destroy_config_table() should return 0!");
}

// Test 2: A repeated cleanup should return 1
void test_destroy_config_table_second_call(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, destroy_config_table(), "The first call to destroy_config_table() should return 0!");
    TEST_ASSERT_EQUAL_INT_MESSAGE(1, destroy_config_table(), "A repeated call to destroy_config_table() should return 1!");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_destroy_config_table_first_call);
    RUN_TEST(test_destroy_config_table_second_call);
    return UNITY_END();
}
