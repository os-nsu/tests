//tests/lab2/config/c_tests/config.h

#ifndef TEST_CONFIG_EXTERNS_H
#define TEST_CONFIG_EXTERNS_H

#include <stdint.h>
#include <stdbool.h>

typedef union {
    int64_t* integer;
    double* real;
    char** string;
} ConfigData;

typedef enum {
    UNDEFINED = 0,
    INTEGER = 1,
    REAL = 2,
    STRING = 3
} ConfigVarType;

typedef struct {
    char* name;
    char* description;
    ConfigData data;
    ConfigVarType type;
    int count;
} ConfigVariable;

extern int create_config_table(void);
extern void destroy_config_table(void);
extern int parse_config(const char *path);
extern int define_variable(ConfigVariable variable);
extern ConfigVariable get_variable(const char *name);
extern int set_variable(ConfigVariable variable);
extern bool does_variable_exist(const char *name);

#endif // TEST_CONFIG_EXTERNS_H
