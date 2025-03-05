// tests/stubs/plugin/greeting_bad_init.c

#include "../../src/include/master.h"
#include <stdio.h>

static Hook last_executor_start_hook = NULL;

void custom_executor_start_hook(void);

const char *name(void) {
    return "greeting";
}

void fini(void) {
    printf("greeting finished\n");
}


void custom_executor_start_hook(void) {
    printf("Hello, world!\n");
}
