// tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_dlsym_name.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

static void* plugin_handle = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, "dlopen(greeting.so) failed");
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
    }
}

void test_plugin_greeting_dlsym_name(void) {
    void* sym = dlsym(plugin_handle, "name");
    TEST_ASSERT_NOT_NULL_MESSAGE(sym, "dlsym(\"name\") returned NULL");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_plugin_greeting_dlsym_name);
    return UNITY_END();
}
