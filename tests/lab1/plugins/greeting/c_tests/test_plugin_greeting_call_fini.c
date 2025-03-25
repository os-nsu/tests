// tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_call_fini.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

typedef void (*plugin_func_void)(void);

static void* plugin_handle = NULL;
static plugin_func_void fini_func = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, "dlopen(greeting.so) failed");

    fini_func = (plugin_func_void)dlsym(plugin_handle, "fini");
    TEST_ASSERT_NOT_NULL_MESSAGE(fini_func, "dlsym(\"fini\") returned NULL");
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
    }
}

void test_plugin_greeting_call_fini(void) {
    fini_func();
    TEST_PASS_MESSAGE("fini() called successfully");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_plugin_greeting_call_fini);
    return UNITY_END();
}
