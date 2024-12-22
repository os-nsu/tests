//tests/lab3/c_tests/test_cache.c

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "cache.h"

#define CACHE_SIZE (1024 * 1024)
#define KEY1 "key1"
#define VALUE1 "value1"
#define VALUE1_SIZE (strlen(VALUE1) + 1)

void test_construct_cache() {
    if (construct_cache(CACHE_SIZE) == 0) {
        printf("[TEST 1] Construct cache: PASS\n");
    } else {
        printf("[TEST 1] Construct cache: FAIL\n");
    }
}

void test_cache_write() {
    if (cache_write(KEY1, VALUE1, VALUE1_SIZE, 0) == 0) {
        printf("[TEST 2] Cache write: PASS\n");
    } else {
        printf("[TEST 2] Cache write: FAIL\n");
    }
}

void test_cache_read_existing_key() {
    size_t value_size;
    char *value = (char*)cache_read(KEY1, &value_size);
    if (value != NULL && strcmp(value, VALUE1) == 0 && value_size == VALUE1_SIZE) {
        printf("[TEST 3] Cache read (existing key): PASS\n");
    } else {
        printf("[TEST 3] Cache read (existing key): FAIL\n");
    }
}

void test_cache_read_missing_key() {
    size_t value_size;
    char *value = (char*)cache_read("unknown_key", &value_size);
    if (value == NULL) {
        printf("[TEST 4] Cache read (missing key): PASS\n");
    } else {
        printf("[TEST 4] Cache read (missing key): FAIL\n");
    }
}

void test_destruct_cache() {
    destruct_cache();
    printf("[TEST 5] Cache destruct: PASS\n");
}

int main() {
    printf("Running cache tests...\n");

    test_construct_cache();
    test_cache_write();
    test_cache_read_existing_key();
    test_cache_read_missing_key();
    test_destruct_cache();

    printf("All cache tests completed.\n");
    return 0;
}
