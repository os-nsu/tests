//tests/lab2/config/c_tests/test_does_variable_exist.c

#include <stdio.h>
#include <stdlib.h>
#include "config.h"
#include "test_assert.h"

int main(void) {
    printf("Running test_does_variable_exist...\n");

    if (create_config_table() != 0) {
        printf("[TEST does_variable_exist] FAIL: create_config_table() failed.\n");
        return 1;
    }

    // Initially, "existing_var" should not exist.
    if (does_variable_exist("existing_var")) {
        printf("[TEST does_variable_exist] FAIL: 'existing_var' reported as existing before definition.\n");
        destroy_config_table();
        return 1;
    } else {
        printf("[TEST does_variable_exist] PASS: 'existing_var' correctly reported as non-existent.\n");
    }

    // Define variable "existing_var".
    ConfigVariable var;
    var.name = "existing_var";
    var.description = "Test existence";
    var.type = INTEGER;
    var.count = 1;
    static int x = 42;
    var.data.integer = &x;

    if (define_variable(var) != 0) {
        printf("[TEST does_variable_exist] FAIL: define_variable(existing_var) failed.\n");
        destroy_config_table();
        return 1;
    }

    // Now it should exist.
    if (!does_variable_exist("existing_var")) {
        printf("[TEST does_variable_exist] FAIL: does_variable_exist(existing_var) returned false.\n");
        destroy_config_table();
        return 1;
    } else {
        printf("[TEST does_variable_exist] PASS: does_variable_exist(existing_var) returned true.\n");
    }

    // Check a non-existent variable.
    if (does_variable_exist("nonexistent_var")) {
        printf("[TEST does_variable_exist] FAIL: does_variable_exist(nonexistent_var) returned true.\n");
        destroy_config_table();
        return 1;
    } else {
        printf("[TEST does_variable_exist] PASS: does_variable_exist(nonexistent_var) returned false.\n");
    }

    destroy_config_table();
    printf("test_does_variable_exist finished.\n");
    return 0;
}
