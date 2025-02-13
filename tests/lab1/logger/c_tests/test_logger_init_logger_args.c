//tests/lab1/logger/c_tests/test_logger_init_logger_args.c

#include <stdio.h>
#include <stdlib.h>
#include "unity.h"
#include "logger.h"

void setUp(void) {
    fini_logger();
}

void tearDown(void) {
    fini_logger();
}

/**
 * Test 1: NULL path and file_size_limit = 0
 *  - The first call is expected to return 0.
 *  - The second call: 1.
 */
void test_init_logger_null_path_zero_limit(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger(NULL, 0),
        "The first call to init_logger(NULL, 0) should return 0!"
    );

    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger(NULL, 0),
        "The second call should return 1!"
    );
}

/**
 * Test 2: NULL path and file_size_limit = -1 (infinity)
 */
void test_init_logger_null_path_infinite_limit(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger(NULL, -1),
        "The first call to init_logger(NULL, -1) should return 0!"
    );
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger(NULL, -1),
        "The second call should return 1!"
    );
}

/**
 * Test 3: Empty string as path ("")
 */
void test_init_logger_empty_path(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger("", 100),
        "The first call to init_logger(\"\", 100) should return 0!"
    );
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger("", 100),
        "The second call should return 1!"
    );
}

/**
 * Test 4: Valid path + small limit
 */
void test_init_logger_valid_path_small_limit(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger("test.log", 100),
        "The first call to init_logger(\"test.log\", 100) should return 0!"
    );
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger("test.log", 100),
        "The second call should return 1!"
    );
}

/**
 * Test 5: Valid path + very large limit
 */
void test_init_logger_valid_path_big_limit(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger("huge_file.log", 999999),
        "The first call to init_logger(\"huge_file.log\", 999999) should return 0!"
    );
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger("huge_file.log", 999999),
        "The second call should return 1!"
    );
}

/**
 * Test 6: "Negative number" not equal to -1 (e.g., -999).
 */
void test_init_logger_weird_negative_limit(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger("somefile.log", -999),
        "The first call to init_logger(\"somefile.log\", -999) should return 1!"
    );
}

/**
 * two calls to init_logger with DIFFERENT arguments"
 */
void test_init_logger_repeated_calls_different_args(void) {
    TEST_ASSERT_EQUAL_INT_MESSAGE(
        0,
        init_logger("fileA.log", 123),
        "The first call to init_logger(\"fileA.log\", 123) should return 0!"
    );

    TEST_ASSERT_EQUAL_INT_MESSAGE(
        1,
        init_logger("fileB.log", 999),
        "The second call (even with different arguments) should still return 1!"
    );
}

int main(void) {
    UNITY_BEGIN();

    RUN_TEST(test_init_logger_null_path_zero_limit);
    RUN_TEST(test_init_logger_null_path_infinite_limit);
    RUN_TEST(test_init_logger_empty_path);
    RUN_TEST(test_init_logger_valid_path_small_limit);
    RUN_TEST(test_init_logger_valid_path_big_limit);
    RUN_TEST(test_init_logger_weird_negative_limit);
    RUN_TEST(test_init_logger_repeated_calls_different_args);

    return UNITY_END();
}
