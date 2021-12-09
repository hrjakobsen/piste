#include "piste.h"
#include <malloc.h>

extern piste_value piste_print(piste_value);
int proc0(closure_t* closure);
extern piste_value piste_add(piste_value, piste_value);
int proc1(closure_t* closure);
int proc2(closure_t* closure);
int proc3(closure_t* closure);
int proc4(closure_t* closure);
int proc5(closure_t* closure);
int proc6(closure_t* closure);

int proc0(closure_t* closure) {
    // print
    piste_value print = closure->free_variables[0];
    piste_value arg_0 = read_message(print);
    piste_value result_channel = read_message(print);
    piste_value result = piste_print(arg_0);
    insert_message(result_channel, result);
    return 1;
}


int proc1(closure_t* closure) {
    // add
    piste_value add = closure->free_variables[0];
    piste_value arg_0 = read_message(add);
    piste_value arg_1 = read_message(add);
    piste_value result_channel = read_message(add);
    piste_value result = piste_add(arg_0, arg_1);
    insert_message(result_channel, result);
    return 1;
}


int proc2(closure_t* closure) {
    // Initialize free variables
    piste_value print = closure->free_variables[0];
    piste_value printer = closure->free_variables[1];

    // Receive message
    if (has_message(printer)) {
        piste_value a = read_message(printer);
        piste_value b = read_message(printer);
        piste_value r = read_message(printer);
        piste_value fresh_1 = alloc_channel();
        insert_message(print, a);
        insert_message(print, fresh_1);

        {
            piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * 4);
            free_vars[0] = b;
            free_vars[1] = fresh_1;
            free_vars[2] = print;
            free_vars[3] = r;
            closure_t* new_closure = alloc_closure(proc3, 4, free_vars);
            queue_process(new_closure);
        }
        return 1;
    } else {
        return 0;
    }
}


int proc3(closure_t* closure) {
    // Initialize free variables
    piste_value b = closure->free_variables[0];
    piste_value fresh_1 = closure->free_variables[1];
    piste_value print = closure->free_variables[2];
    piste_value r = closure->free_variables[3];

    // Receive message
    if (has_message(fresh_1)) {
        piste_value _ = read_message(fresh_1);
        piste_value fresh_0 = alloc_channel();
        insert_message(print, b);
        insert_message(print, fresh_0);

        {
            piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * 2);
            free_vars[0] = fresh_0;
            free_vars[1] = r;
            closure_t* new_closure = alloc_closure(proc4, 2, free_vars);
            queue_process(new_closure);
        }
        return 1;
    } else {
        return 0;
    }
}


int proc4(closure_t* closure) {
    // Initialize free variables
    piste_value fresh_0 = closure->free_variables[0];
    piste_value r = closure->free_variables[1];

    // Receive message
    if (has_message(fresh_0)) {
        piste_value _ = read_message(fresh_0);
        insert_message(r, (piste_value){ .type = INT, .value = 2});
        return 1;
    } else {
        return 0;
    }
}


int proc5(closure_t* closure) {
    // Initialize free variables
    piste_value fresh_3 = closure->free_variables[0];
    piste_value print = closure->free_variables[1];

    // Receive message
    if (has_message(fresh_3)) {
        piste_value result = read_message(fresh_3);
        piste_value fresh_2 = alloc_channel();
        insert_message(print, result);
        insert_message(print, fresh_2);

        {
            piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * 1);
            free_vars[0] = fresh_2;
            closure_t* new_closure = alloc_closure(proc6, 1, free_vars);
            queue_process(new_closure);
        }
        return 1;
    } else {
        return 0;
    }
}


int proc6(closure_t* closure) {
    // Initialize free variables
    piste_value fresh_2 = closure->free_variables[0];

    // Receive message
    if (has_message(fresh_2)) {
        piste_value _ = read_message(fresh_2);
        /* inaction */
        return 1;
    } else {
        return 0;
    }
}


int piste_entry(closure_t* closure) {

    piste_value print = alloc_channel();
    {
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value));
        free_vars[0] = print;
        closure_t* new_closure = alloc_closure(proc0, 1, free_vars);
        add_replicated_reader(new_closure, print);
    }


    piste_value add = alloc_channel();
    {
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value));
        free_vars[0] = add;
        closure_t* new_closure = alloc_closure(proc1, 1, free_vars);
        add_replicated_reader(new_closure, add);
    }

    piste_value printer = alloc_channel();

    {
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * 2);
        free_vars[0] = print;
        free_vars[1] = printer;
        closure_t* new_closure = alloc_closure(proc2, 2, free_vars);
        add_replicated_reader(new_closure, printer);
    }

    piste_value fresh_3 = alloc_channel();
    insert_message(printer, (piste_value){ .type = STRING, .value = (long) "test af en stor fed hest! :)" });
    insert_message(printer, (piste_value){ .type = STRING, .value = (long) "hest" });
    insert_message(printer, fresh_3);

    {
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * 2);
        free_vars[0] = fresh_3;
        free_vars[1] = print;
        closure_t* new_closure = alloc_closure(proc5, 2, free_vars);
        queue_process(new_closure);
    };
    return 1;
}