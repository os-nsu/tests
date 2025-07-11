// tests/regression/c_tests/segfault_message.c

#include <stdio.h>

int main(void)
{
    puts("SEGFAULT-LINE");
    int *p = NULL;
    *p = 42;
    return 0;
}
