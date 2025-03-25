// File: tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_call_init.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

typedef void (*plugin_func_void)(void);

static void *plugin_handle = NULL;
static plugin_func_void init_func = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL(plugin_handle);
    init_func = (plugin_func_void)dlsym(plugin_handle, "init");
    TEST_ASSERT_NOT_NULL(init_func);
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
        plugin_handle = NULL;
    }
}

void test_call_init(void) {
    init_func();
    TEST_PASS_MESSAGE("init() called successfully");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_call_init);
    return UNITY_END();
}
