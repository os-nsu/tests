// tests/lab1/plugins/greeting/test_plugin_greeting.c

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <string.h>

/* Prototype of functions in greeting.so:
   void init(void);
   void fini(void);
   const char* name(void);
*/
typedef void (*Hook)(void);

Hook executor_start_hook = NULL;
Hook executor_end_hook   = NULL;

typedef void (*plugin_func_void)(void);
typedef const char* (*plugin_func_name)(void);

int main(void) {
    printf("Running test_plugin_greeting...\n");

    printf("[TEST 1] dlopen(greeting.so): ");
    void* handle = dlopen("greeting.so", RTLD_NOW | RTLD_LOCAL);
    if (!handle) {
        printf("FAIL (error: %s)\n", dlerror());
        return 1;
    }
    printf("PASS\n");

    printf("[TEST 2] dlsym(\"init\"): ");
    plugin_func_void init_func = (plugin_func_void)dlsym(handle, "init");
    if (!init_func) {
        printf("FAIL (error: %s)\n", dlerror());
        dlclose(handle);
        return 1;
    }
    printf("PASS\n");

    printf("[TEST 3] dlsym(\"name\"): ");
    plugin_func_name name_func = (plugin_func_name)dlsym(handle, "name");
    if (!name_func) {
        printf("FAIL (error: %s)\n", dlerror());
        dlclose(handle);
        return 1;
    }
    printf("PASS\n");

    printf("[TEST 4] dlsym(\"fini\"): ");
    plugin_func_void fini_func = (plugin_func_void)dlsym(handle, "fini");
    if (!fini_func) {
        printf("FAIL (error: %s)\n", dlerror());
        dlclose(handle);
        return 1;
    }
    printf("PASS\n");

    printf("[TEST 5] calling init()...\n");
    init_func();
    printf("[TEST 5] init() returned: PASS\n");

    printf("[TEST 6] calling name()...\n");
    const char* pname = name_func();
    if (pname) {
        printf("[TEST 6] name() returned: PASS (got: %s)\n", pname);
    } else {
        printf("[TEST 6] name() returned: FAIL (NULL)\n");
        dlclose(handle);
        return 1;
    }

    printf("[TEST 7] calling fini()...\n");
    fini_func();
    printf("[TEST 7] fini() returned: PASS\n");

    printf("[TEST 8] dlclose(handle): ");
    dlclose(handle);
    printf("PASS\n");

    printf("test_plugin_greeting finished.\n");
    return 0;
}
