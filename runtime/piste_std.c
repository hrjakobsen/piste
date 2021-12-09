//
// Created by mathias on 04/12/2021.
//
#include "piste_std.h"
#include <stdio.h>

piste_value piste_print(piste_value val) {
    switch (val.type) {
        case INT:
            printf("%ld\n", val.value);
            break;
        case BOOL:
            printf(val.value == 1 ? "true\n" : "false\n");
            break;
        case CHANNEL:
            printf("channel (0x%lx)\n", val.value);
            break;
        case STRING:
            printf("%s\n", (char*)val.value);
            break;
        case RECORD:
            printf("record (0x%lx)\n", val.value);
    }
    return (piste_value) {
        .type = BOOL,
        .value = 1
    };
}

piste_value piste_add(piste_value v1, piste_value v2) {
    return (piste_value) { .type= INT, .value = v1.value + v2.value };
}

