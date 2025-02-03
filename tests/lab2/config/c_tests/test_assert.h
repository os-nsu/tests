#ifndef TEST_ASSERT_H
#define TEST_ASSERT_H

#include <stdio.h>

static inline int assert_eq_impl(const char* file, int line, const char* test_name, int actual, int expected) {
    if (actual != expected) {
        printf("[%s] FAIL (%s:%d, expected=%d, got=%d)\n", test_name, file, line, expected, actual);
        return -1;
    } else {
        printf("[%s] PASS\n", test_name);
        return 0;
    }
}

#define ASSERT_EQUAL(test_name, actual, expected) \
    do { \
        if (assert_eq_impl(__FILE__, __LINE__, test_name, (actual), (expected)) != 0) return -1; \
    } while (0)

#endif /* TEST_ASSERT_H */
