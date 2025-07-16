#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 256*1024; ++i)
    {
        putchar('A');
    }
    return 0;
}
