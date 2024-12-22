//test_cache.c


#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "alloc.h"

#define ALLOCATOR_SIZE (1024 * 1024)
#define SIMPLE_ALLOCATION_SIZE 128
#define LARGE_ALLOCATION_SIZE (10 * 1024 * 1024)

void test_allocator_init() {
    if (my_allocator_init(ALLOCATOR_SIZE) == 0) {
        printf("[TEST 1] Allocator initialization: PASS\n");
    } else {
        printf("[TEST 1] Allocator initialization: FAIL\n");
    }
}

void test_simple_allocation() {
    void *p = my_malloc(SIMPLE_ALLOCATION_SIZE);
    if (p != NULL) {
        printf("[TEST 2] Simple allocation: PASS\n");
        memset(p, 0xAA, SIMPLE_ALLOCATION_SIZE);
        my_free(p);
        printf("[TEST 3] Simple deallocation: PASS\n");
    } else {
        printf("[TEST 2] Simple allocation: FAIL\n");
    }
}

void test_large_allocation() {
    void *p = my_malloc(LARGE_ALLOCATION_SIZE);
    if (p == NULL) {
        printf("[TEST 4] Large allocation (expected failure): PASS\n");
    } else {
        printf("[TEST 4] Large allocation (expected failure): FAIL\n");
    }
}

void test_invalid_free() {
    my_free(NULL);
    printf("[TEST 5] Free NULL pointer: PASS\n");
}

int main() {
    printf("Running allocator tests...\n");
    test_allocator_init();
    test_simple_allocation();
    test_large_allocation();
    test_invalid_free();
    printf("All tests finished.\n");
    return 0;
}
