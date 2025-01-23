// tests/lab1/logger/test_logger.c

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

extern int init_logger(void);

int main(void) {
    printf("Running test_logger...\n");

    int result;

    result = init_logger();
    if (result == 0) {
        printf("[TEST 1] init_logger first call: PASS\n");
    } else {
        printf("[TEST 1] init_logger first call: FAIL (got %d)\n", result);
    }

    printf("test_logger finished.\n");
    return 0;
}
