// tests/lab2/config/c_tests/test_config_parse.c

#include <stdio.h>
#include <stdlib.h>

#include "config.h"
#include "test_assert.h"

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

int main(void) {
    printf("Running test_config_parse...\n");

    if (create_config_table() != 0) {
        printf("[TEST parse_config] FAIL: create_config_table() failed.\n");
        return 1;
    }

    // [TEST 1] Passing NULL to parse_config should return -1 (invalid input)
    int return_value = parse_config(NULL);
    ASSERT_EQUAL("TEST 1 parse_config(NULL)", return_value, -1);

    // [TEST 2] Passing a non-existent file should return -1
    return_value = parse_config("not_config.conf");
    ASSERT_EQUAL("TEST 2 parse_config(not_config.conf)", return_value, -1);

    // [TEST 3] Parsing a valid configuration file should return 0
    //Create config file
    FILE *fp = fopen("config.conf", "w");
    if (!fp) {
        printf("[SETUP] FAIL: Unable to create config.conf file.\n");
        destroy_config_table();
        return 1;
    }

    // Write valid configuration parameters:
    // log_file_size_limit = 2048
    // log_dir = "my_logs"
    // plugins = ["greeting"]
    fprintf(fp, "log_file_size_limit = 2048\n");
    fprintf(fp, "log_dir = \"my_logs\"\n");
    fprintf(fp, "plugins = [\"greeting\"\n");
    fclose(fp);

    //TEST[3]
    return_value = parse_config("config.conf");
    ASSERT_EQUAL("TEST 3 parse_config(config.conf)", return_value, 0);

    destroy_config_table();
    remove("config.conf");

    printf("test_config_parse finished.\n");
    return 0;
}
