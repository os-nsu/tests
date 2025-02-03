// tests/lab2/config/c_tests/test_config_define.c

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "config.h"
#include "test_assert.h"

int main(void) {
    printf("Running test_config_define...\n");

    if (create_config_table() != 0) {
        printf("[SETUP] create_config_table() failed\n");
        return 1;
    }

    // [TEST 1] Define a new configuration variable: my_int = 123
    ConfigVariable var;
    var.name = "my_int";
    var.description = "test int";
    var.type = INTEGER;
    var.count = 1;

    static int64_t val = 123;
    var.data.integer = &val;

    int return_value = define_variable(var);
    ASSERT_EQUAL("TEST 1 define_variable(my_int=123)", return_value, 0);


    // [TEST 2] Attempt to define the same variable again with a different value should fail
    static int64_t val2 = 999;
    var.data.integer = &val2;
    return_value = define_variable(var);
    ASSERT_EQUAL("TEST 2 define_variable(my_int=999 again)", return_value, -1);

    destroy_config_table();

    printf("test_config_define finished.\n");
    return 0;
}
