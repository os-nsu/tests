//tests/lab2/config/c_tests/test_config_set_variable.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "test_assert.h"

int main(void) {
    printf("Running test_set_variable...\n");

    if (create_config_table() != 0) {
        printf("[TEST set_variable] FAIL: create_config_table() failed.\n");
        return 1;
    }

    // Define a string variable "my_str" with initial value "hello".
    ConfigVariable var;
    var.name = "my_str";
    var.description = "Test string variable update";
    var.type = STRING;
    var.count = 1;
    char *initial = "hello";
    var.data.string = &initial;

    if (define_variable(var) != 0) {
        printf("[TEST set_variable] FAIL: define_variable(my_str) failed.\n");
        destroy_config_table();
        return 1;
    }

    // Update "my_str" to "world".
    char *updated = "world";
    ConfigVariable new_var;
    new_var.name = "my_str";
    new_var.description = "Test string variable update";
    new_var.type = STRING;
    new_var.count = 1;
    new_var.data.string = &updated;

    if (set_variable(new_var) != 0) {
        printf("[TEST set_variable] FAIL: set_variable(my_str) failed.\n");
        destroy_config_table();
        return 1;
    }

    // Retrieve and verify updated value.
    ConfigVariable ret_var = get_variable("my_str");
    if (strcmp(ret_var.data.string[0], "world") != 0) {
        printf("[TEST set_variable] FAIL: Expected value 'world', got '%s'.\n", ret_var.data.string[0]);
        destroy_config_table();
        return 1;
    }

    printf("[TEST set_variable] PASS: set_variable updated the value correctly.\n");
    destroy_config_table();
    printf("test_set_variable finished.\n");
    return 0;
}
