// tests/stubs/good/plugin/greeting/greeting_good_init.c

#include "../../src/include/master.h"
#include <stdio.h>

extern Hook last_executor_start_hook;

static void custom_executor_start_hook(void) {
    if (last_executor_start_hook) {
        last_executor_start_hook();
    }
    printf("Hello, world!\n");
}

void init(void) {
    last_executor_start_hook = executor_start_hook;

    executor_start_hook = custom_executor_start_hook;

    printf("greeting initialized\n");
}