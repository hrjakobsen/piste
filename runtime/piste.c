#include "piste.h"
#include <stdio.h>
#include <assert.h>
#include <malloc.h>
#include <memory.h>

run_queue_t* RUN_QUEUE = NULL;
run_queue_t* BLOCKED_LIST = NULL;
replicated_reader_t* REPLICATED_READERS_HEAD = NULL;
replicated_reader_t* REPLICATED_READERS_END = NULL;

extern int piste_entry(closure_t*);

void initialize_run_queue();

void spawn_readers();

closure_t *copy_closure(struct closure *pClosure);

void move_replicated_reader_to_end(replicated_reader_t *reader);

piste_value alloc_channel() {
    piste_channel* channel_ptr = malloc(sizeof(piste_channel));
    channel_ptr->num_messages = 0;
    channel_ptr->message_list = NULL;
    piste_value channel_val = {
            .type = CHANNEL,
            .value = (piste_int_t)channel_ptr,
    };
    return channel_val;
}

void insert_message(piste_value receiver, piste_value message) {
    assert(receiver.type == CHANNEL);
    piste_channel* channel = (piste_channel *)(receiver.value);

    channel_node* node_ptr = malloc(sizeof(channel_node));

    node_ptr->message = message;
    node_ptr->next = NULL;

    if (channel->num_messages == 0) {
        channel->message_list = node_ptr;
    } else {
        channel_node* list_ptr = channel->message_list;
        // Find end of list
        while (list_ptr->next != NULL)
            list_ptr = list_ptr->next;
        list_ptr->next = node_ptr;
    }

    channel->num_messages++;
}

int has_message(piste_value receiver) {
    assert(receiver.type == CHANNEL);
    piste_channel* channel = (piste_channel *)(receiver.value);
    return channel->num_messages > 0;
}

piste_value read_message(piste_value receiver) {
    assert(receiver.type == CHANNEL);
    piste_channel* channel = (piste_channel *)(receiver.value);
    assert(channel->num_messages > 0);
    channel_node* head = channel->message_list;
    channel_node* tail = head->next;
    piste_value result = head->message;
    free(head);
    channel->message_list = tail;
    channel->num_messages--;
    return result;
}

closure_t* alloc_closure(proc_t proc, size_t num_free_variables, piste_value *free_variables) {
    closure_t* closure = (closure_t*)malloc(sizeof(closure_t));
    closure->num_vars = num_free_variables;
    closure->proc = proc;
    closure->free_variables = free_variables;
    return closure;
}

void queue_process(closure_t *closure) {
    run_queue_t* next = malloc(sizeof(run_queue_t));
    next->next = NULL;
    next->closure = closure;
    if (RUN_QUEUE == NULL) {
        // Make new empty list
        RUN_QUEUE = next;
    } else {
        // Insert at end of queue
        run_queue_t* last = RUN_QUEUE;
        while (last->next != NULL)
            last = last->next;
        last->next = next;
    }
}

void block_process(closure_t *closure) {
    run_queue_t* next = malloc(sizeof(run_queue_t));
    next->next = NULL;
    next->closure = closure;
    if (BLOCKED_LIST == NULL) {
        // Make new empty list
        BLOCKED_LIST = next;
    } else {
        // Insert at end of queue
        run_queue_t* last = BLOCKED_LIST;
        while (last->next != NULL)
            last = last->next;
        last->next = next;
    }
}

void unblock_processes() {
    if (RUN_QUEUE == NULL) {
        RUN_QUEUE = BLOCKED_LIST;
        BLOCKED_LIST = NULL;
        return;
    }
    run_queue_t* last = RUN_QUEUE;
    while (last->next != NULL)
        last = last->next;
    last->next = BLOCKED_LIST;
    BLOCKED_LIST = NULL;
}

closure_t* deque_process() {
    assert(RUN_QUEUE != NULL);
    run_queue_t* first = RUN_QUEUE;
    RUN_QUEUE = first->next;
    closure_t* closure = first->closure;
    free(first);
    return closure;
}

int main(int argc, char** argv) {
    initialize_run_queue();

    while (RUN_QUEUE != NULL) {
        closure_t* closure = deque_process();
        int finished = closure->proc(closure);
        if (finished) {
            free(closure->free_variables);
            free(closure);
        } else {
            block_process(closure);
        }

        if (RUN_QUEUE == NULL) {
            spawn_readers();
            unblock_processes();
        }
    }
    printf("done");
}

void spawn_readers() {
    for (replicated_reader_t* cur = REPLICATED_READERS_HEAD; cur != NULL; cur = cur->next) {
        piste_channel* chn = (piste_channel*) cur->channel.value;
        if (has_message(cur->channel)) {
            // We should spawn a reader
            queue_process(copy_closure(cur->closure));
            // Now move replicated reader to end
            move_replicated_reader_to_end(cur);
            return;
        }
    }
}

void move_replicated_reader_to_end(replicated_reader_t *reader) {
    if (REPLICATED_READERS_END == NULL || REPLICATED_READERS_END == reader) {
        return;
    }
    if (REPLICATED_READERS_HEAD == reader) {
        // We are the first element
        if (reader->next == NULL) {
            // We are the *only* element
            return;
        }
        reader->next->previous = NULL;
        reader->previous = REPLICATED_READERS_END;
        REPLICATED_READERS_END->next = reader;
        REPLICATED_READERS_HEAD = reader->next;
        reader->next = NULL;
        REPLICATED_READERS_END = reader;
    } else {
        // We are in the middle
        reader->previous->next = reader->next;
        reader->next->previous = reader->previous;
        reader->previous = REPLICATED_READERS_END;
        reader->next = NULL;
        REPLICATED_READERS_END->next = reader;
        REPLICATED_READERS_END = reader;
    }
}

closure_t* copy_closure(closure_t *closure) {
    closure_t* new_closure = (closure_t*) malloc(sizeof(closure_t));
    size_t arr_size = sizeof(piste_value) * closure->num_vars;
    new_closure->proc = closure->proc;
    new_closure->num_vars = closure->num_vars;
    new_closure->free_variables = malloc(arr_size);
    memcpy(new_closure->free_variables, closure->free_variables, arr_size);
    return new_closure;
}

void initialize_run_queue() {
    closure_t* closure = alloc_closure(piste_entry, 0, NULL);
    RUN_QUEUE = malloc(sizeof(run_queue_t));
    RUN_QUEUE->closure = closure;
    RUN_QUEUE->next = NULL;
}

void add_replicated_reader(closure_t* closure, piste_value channel) {
    replicated_reader_t * node = (replicated_reader_t*) malloc(sizeof(replicated_reader_t));
    node->next = NULL;
    node->closure = closure;
    node->channel = channel;

    if (REPLICATED_READERS_HEAD == NULL) {
        node->previous = NULL;
        REPLICATED_READERS_HEAD = node;
        REPLICATED_READERS_END = node;
        return;
    } else {
        node->previous = REPLICATED_READERS_END;
    }

    REPLICATED_READERS_END->next = node;
    REPLICATED_READERS_END = node;
}
