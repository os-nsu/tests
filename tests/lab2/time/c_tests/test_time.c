// tests/lab2/time/c_tests/test_time.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "my_time.h"
#include <time.h>
#include <unistd.h>

#define TIMEOUT_DIFF 1

void setUp(void) {
}

void tearDown(void) {
}

// Test 1: Ensure the syscall library works correctly and is consistent with system time
void test_time_syscall(void) {
    time_t returned_time = get_time();
    time_t system_time = time(NULL);

    TEST_ASSERT_GREATER_THAN_MESSAGE(0, returned_time, "Returned time is invalid (should be > 0)");

    TEST_ASSERT_LESS_OR_EQUAL_MESSAGE(TIMEOUT_DIFF, abs(returned_time - system_time),
        "Returned time is not within timeout seconds of system time");
}

// Test 2: Check that get_time() returns different values on multiple calls
void test_multiple_calls(void) {
    time_t first_time = get_time();
    sleep(1);
    time_t second_time = get_time();

    TEST_ASSERT_NOT_EQUAL_MESSAGE(first_time, second_time, "Subsequent calls returned the same time value");
}

int main(void) {
    UNITY_BEGIN();

    RUN_TEST(test_time_syscall);
    RUN_TEST(test_multiple_calls);

    return UNITY_END();
}
