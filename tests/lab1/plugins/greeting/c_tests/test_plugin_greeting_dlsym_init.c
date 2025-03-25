// tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_dlsym_init.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

static void *plugin_handle = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, "dlopen greeting.so failed");
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
        plugin_handle = NULL;
    }
}

void test_dlsym_init(void) {
    void* sym = dlsym(plugin_handle, "init");
    TEST_ASSERT_NOT_NULL_MESSAGE(sym, "dlsym(\"init\") failed");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_dlsym_init);
    return UNITY_END();
}
