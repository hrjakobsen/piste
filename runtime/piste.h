#ifndef PISTE_PISTE_H
#define PISTE_PISTE_H
#include <stdint.h>
#include <stddef.h>

typedef long piste_int_t;

enum piste_value_t {
    INT,
    BOOL,
    CHANNEL,
    STRING,
    RECORD,
    VOID,
    LIST,
};

typedef enum piste_value_t piste_value_t;

struct piste_value {
    piste_value_t type;
    // value can be an actual value (for int and bool)
    // or a pointer to a heap allocated value (channel, record, string)
    piste_int_t value;
};


typedef struct piste_value piste_value;

static const piste_value UNIT = (piste_value) {.type = VOID, .value = 0 };

struct channel_node {
    struct channel_node* next;
    piste_value message;
};

typedef struct channel_node channel_node;

struct piste_channel {
    int num_messages;
    channel_node* message_list;
};

typedef struct piste_channel piste_channel;

struct piste_linked_list {
    struct piste_linked_list* next;
    piste_value element;
};

typedef struct piste_linked_list piste_linked_list;

struct piste_list {
    size_t num_elements;
    piste_linked_list* elements;
};

typedef struct piste_list piste_list;

struct closure;

typedef int (*proc_t)(struct closure*);

struct closure {
    proc_t proc;
    size_t num_vars;
    piste_value* free_variables;
};

typedef struct closure closure_t;

struct run_queue {
    struct run_queue* next;
    struct closure* closure;
};

typedef struct run_queue run_queue_t;

struct replicated_reader {
    piste_value channel;
    struct replicated_reader* next;
    struct replicated_reader* previous;
    struct closure* closure;
};

typedef struct replicated_reader replicated_reader_t;


void insert_message(piste_value receiver, piste_value message);
int has_message(piste_value);
piste_value read_message(piste_value);
piste_value alloc_channel();
closure_t* alloc_closure(proc_t, size_t num_free_variables, piste_value* free_variables);
void queue_process(closure_t* closure);
void add_replicated_reader(closure_t*, piste_value);
piste_value list_get(piste_value list_value, piste_value index);
piste_value alloc_list_with_elements(int, piste_value elements[]);
piste_value append_lists(piste_value, piste_value);


enum exit_code {
    LIST_OUT_OF_RANGE = 0
};

typedef enum exit_code exit_code;

#endif //PISTE_PISTE_H
