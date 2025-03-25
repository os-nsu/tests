// tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_dlopen.c

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

static void* plugin_handle = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = NULL;
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
    }
}

void test_dlopen_plugin(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, "dlopen failed - greeting.so not found or can't be loaded");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_dlopen_plugin);
    return UNITY_END();
}
