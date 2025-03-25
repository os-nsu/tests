// File: tests/lab1/plugins/greeting/c_tests/test_plugin_greeting_dlclose.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

static void *plugin_handle = NULL;

Hook executor_start_hook = NULL;

void setUp(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL(plugin_handle);
}

void tearDown(void) {
}

// Тест
void test_dlclose(void) {
    int rc = dlclose(plugin_handle);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, rc, "dlclose() failed");
    plugin_handle = NULL;
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_dlclose);
    return UNITY_END();
}
