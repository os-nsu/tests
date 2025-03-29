// tests/stubs/good/plugin/greeting/greeting_good_fini.c

#include "../../src/include/master.h"
#include <stdio.h>

extern Hook last_executor_start_hook;

void fini(void) {
    executor_start_hook = last_executor_start_hook;
    printf("greeting finished\n");
}