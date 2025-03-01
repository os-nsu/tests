// tests/lab2/logger/c_tests/test_logger_file_stream_rollover.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "unity.h"
#include "logger.h"

/*
  Purpose: Verify that if file_size_limit is small (e.g., 2 KB),
  and a new entry "doesn't fit" (e.g., 3 KB), the file is truncated
  and the entry is written from the beginning.

  Implementation detail: we call init_logger(<filename>, 2), meaning 2 KB limit.
  We first write a small message, then we write a large                         ~3 KB message.
  The logger should detect that (current_size + new_entry > limit)
  and do a "truncate" before writing. write_log() must still return 0 (success).
*/

char *LOG_FILENAME = "rollover_test.log";

void setUp(void) {
    // init_logger with 2 KB limit
    // (Remember: 1 means infinite, so 2 is minimal actual limit)
    int ret = init_logger(LOG_FILENAME, 2);
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "init_logger() with limit=2KB must return 0 on success");
}

void tearDown(void) {
    int ret = fini_logger();
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, ret, "fini_logger() must return 0 if logger wasn't freed yet");
}

void test_file_rollover(void) {
    // 1) Write a small line (say ~50 bytes including the log header overhead).
    int w1 = write_log(FILESTREAM, LOG_INFO, __FILE__, __LINE__,
                       "First short line: ~under 2KB");
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, w1, "First write_log() must return 0");

    // 2) Write a large message (~3 KB). We'll build it dynamically in memory:
    //    The overhead from the logger is also added, so it definitely exceeds 2 KB total.
    char large_msg[3000];
    memset(large_msg, 'A', sizeof(large_msg) - 1);
    large_msg[sizeof(large_msg) - 1] = '\0';

    int w2 = write_log(FILESTREAM, LOG_INFO, __FILE__, __LINE__,
                       "Second line, definitely bigger than 2KB: %s", large_msg);

    // The logger should detect overflow, clear the file, and then write.
    // So the operation is still "successful", returning 0.
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, w2,
        "Second write_log() with big message must return 0, indicating success.");
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_file_rollover);
    return UNITY_END();
}
