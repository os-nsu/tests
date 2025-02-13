// tests/lab1/plugins/greeting/test_plugin_greeting.c

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <dlfcn.h>
#include "unity.h"
#include "master.h"

static void* plugin_handle = NULL;

Hook executor_start_hook = NULL;

typedef void (*plugin_func_void)(void);
typedef const char* (*plugin_func_name)(void);

void setUp(void) {
}

void tearDown(void) {
}

void test_dlopen(void) {
    plugin_handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    TEST_ASSERT_NOT_NULL_MESSAGE(plugin_handle, dlerror());
}

void test_dlsym_init(void) {
    void* sym = dlsym(plugin_handle, "init");
    TEST_ASSERT_NOT_NULL_MESSAGE(sym, "dlsym(\"init\") failed");
}

void test_dlsym_name(void) {
    void* sym = dlsym(plugin_handle, "name");
    TEST_ASSERT_NOT_NULL_MESSAGE(sym, "dlsym(\"name\") failed");
}

void test_dlsym_fini(void) {
    void* sym = dlsym(plugin_handle, "fini");
    TEST_ASSERT_NOT_NULL_MESSAGE(sym, "dlsym(\"fini\") failed");
}

void test_call_init(void) {
    plugin_func_void init_func = (plugin_func_void)dlsym(plugin_handle, "init");
    TEST_ASSERT_NOT_NULL_MESSAGE(init_func, "dlsym(\"init\") returned NULL");
    init_func();
    TEST_PASS_MESSAGE("init() called successfully");
}

void test_call_name(void) {
    plugin_func_name name_func = (plugin_func_name)dlsym(plugin_handle, "name");
    TEST_ASSERT_NOT_NULL_MESSAGE(name_func, "dlsym(\"name\") returned NULL");
    const char* pname = name_func();
    TEST_ASSERT_NOT_NULL_MESSAGE(pname, "name() returned NULL");
    TEST_ASSERT_EQUAL_STRING_MESSAGE("greeting", pname, "name() did not return expected string");
}

void test_call_fini(void) {
    plugin_func_void fini_func = (plugin_func_void)dlsym(plugin_handle, "fini");
    TEST_ASSERT_NOT_NULL_MESSAGE(fini_func, "dlsym(\"fini\") returned NULL");
    fini_func();
    TEST_PASS_MESSAGE("fini() called successfully");
}

void test_dlclose(void) {
    int res = dlclose(plugin_handle);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, res, "dlclose() failed");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_dlopen);
    RUN_TEST(test_dlsym_init);
    RUN_TEST(test_dlsym_name);
    RUN_TEST(test_dlsym_fini);
    RUN_TEST(test_call_init);
    RUN_TEST(test_call_name);
    RUN_TEST(test_call_fini);
    RUN_TEST(test_dlclose);
    return UNITY_END();
}
