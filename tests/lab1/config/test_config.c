// tests/lab1/config/test_config.c

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

extern int create_config_table(void);

int main(void) {
    printf("Running test_config...\n");

    int result;

    result = create_config_table();
    if (result == 0) {
        printf("[TEST 1] create_config_table first call: PASS\n");
    } else {
        printf("[TEST 1] create_config_table first call: FAIL (got %d)\n", result);
    }

    printf("test_config finished.\n");
    return 0;
}
