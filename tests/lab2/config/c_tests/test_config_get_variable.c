//tests/lab2/config/c_tests/test_config_get_variable.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "test_assert.h"

int main(void) {
    printf("Running test_get_variable...\n");

    if (create_config_table() != 0) {
        printf("[TEST get_variable] FAIL: create_config_table() failed.\n");
        return 1;
    }

    // Define a string variable "my_str" with value "hello".
    ConfigVariable var;
    var.name = "my_str";
    var.description = "Test string variable";
    var.type = STRING;
    var.count = 1;
    char *value = "hello";
    var.data.string = &value;

    if (define_variable(var) != 0) {
        printf("[TEST get_variable] FAIL: define_variable(my_str) failed.\n");
        destroy_config_table();
        return 1;
    }

    // Retrieve the variable.
    ConfigVariable ret_var = get_variable("my_str");
    if (ret_var.type != STRING) {
        printf("[TEST get_variable] FAIL: Expected type STRING for my_str.\n");
        destroy_config_table();
        return 1;
    }
    if (ret_var.count != 1) {
        printf("[TEST get_variable] FAIL: Expected count 1 for my_str, got %d.\n", ret_var.count);
        destroy_config_table();
        return 1;
    }
    if (strcmp(ret_var.data.string[0], "hello") != 0) {
        printf("[TEST get_variable] FAIL: Expected value 'hello' for my_str, got '%s'.\n", ret_var.data.string[0]);
        destroy_config_table();
        return 1;
    }

    printf("[TEST get_variable] PASS: get_variable returned correct value.\n");
    destroy_config_table();
    printf("test_get_variable finished.\n");
    return 0;
}
