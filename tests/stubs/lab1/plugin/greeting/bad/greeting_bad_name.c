// tests/stubs/plugin/greeting_bad_name.c

#include "../../src/include/master.h"
#include <stdio.h>

static Hook last_executor_start_hook = NULL;

void custom_executor_start_hook(void);

void init(void) {
    last_executor_start_hook = executor_start_hook;
    executor_start_hook = custom_executor_start_hook;
    printf("greeting initialized\n");
}

void fini(void) {
    executor_start_hook = last_executor_start_hook;
    printf("greeting finished\n");
}

void custom_executor_start_hook(void) {
    printf("Hello, world!\n");
}
