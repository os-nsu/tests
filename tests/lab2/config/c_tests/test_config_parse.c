// tests/lab2/config/c_tests/test_config_parse.c

#include <stdio.h>
#include <stdlib.h>


static void check_result(const char* test_name, int actual, int expected) {
    if (actual == expected) {
        printf("[%s] PASS\n", test_name);
    } else {
        printf("[%s] FAIL (expected=%d, got=%d)\n", test_name, expected, actual);
        exit(1);
    }
}

extern int create_config_table(void);
extern int parse_config(const char* path);
extern int destroy_config_table(void);

int main(void) {
    printf("Running test_config_parse...\n");

    int return_value = create_config_table();
    if (return_value != 0) {
        printf("[SETUP] FAIL create_config_table()\n");
        return 1;
    }

    // [TEST 1] parse_config(NULL) => -1
    return_value = parse_config(NULL);
    check_result("TEST 1 parse_config(NULL)", return_value, -1);

    // [TEST 2] parse_config("not_config.conf") => -1
    return_value = parse_config("not_config.conf");
    check_result("TEST 2 parse_config(not_config.conf)", return_value, -1);

    // [TEST 3] parse_config("config.conf") => 0
    return_value = parse_config("config.conf");
    check_result("TEST 3 parse_config(config.conf)", return_value, 0);

    destroy_config_table();

    printf("test_config_parse finished.\n");
    return 0;
}
