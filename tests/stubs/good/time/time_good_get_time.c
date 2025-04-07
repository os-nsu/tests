// tests/stubs/good/time/time_good_get_time.c

#include "my_time.h"

/* Good stub implementation for lab1.
 * Returns a current time .
 */
time_t get_time(void) {
    return time(NULL);
}
