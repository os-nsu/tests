// tests/stubs/time/time_stub.c

#include <time.h>

/* Stub implementation for lab1.
 * Returns a fixed timestamp (e.g., 0) so that get_time is defined.
 */
time_t get_time(void) {
    return 1609459200;
}
