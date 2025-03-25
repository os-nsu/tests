// tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_call_name.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

typedef const char* (*plugin_func_name)(void);

static void* plugin_handle = NULL;
static plugin_func_name name_func = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, "dlopen(greeting.so) failed");

    name_func = (plugin_func_name)dlsym(plugin_handle, "name");
    TEST_ASSERT_NOT_NULL_MESSAGE(name_func, "dlsym(\"name\") returned NULL");
}

void tearDown(void) {
    if (plugin_handle) {
        dlclose(plugin_handle);
    }
}

void test_plugin_greeting_call_name(void) {
    const char* pname = name_func();
    TEST_ASSERT_NOT_NULL_MESSAGE(pname, "name() returned NULL");
    TEST_ASSERT_EQUAL_STRING_MESSAGE("greeting", pname, "Expected plugin name = 'greeting'");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_plugin_greeting_call_name);
    return UNITY_END();
}
