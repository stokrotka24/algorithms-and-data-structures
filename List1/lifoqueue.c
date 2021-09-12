#include <stdio.h>
#include <malloc.h>

typedef struct Elem {
    int value;
    struct Elem *prev;
} Node;

int size(Node *top) {
    int size = 0;

    while (top != NULL) {
        size++;
        top = top->prev;
    }
    return size;
}

int is_empty(Node *top) {
    return top == NULL;
}

void push(Node **top, int val) {
    Node *new_top = malloc(sizeof(Node));
    new_top->value = val;
    new_top->prev = *top;
    *top = new_top;

    printf("Adding %d\n", val);
}

void pop(Node **top) {
    if (is_empty(*top)) {
        printf("Nothing to pop\n");
    } else {
        Node *deleted_node = *top;
        printf("Popping %d\n", deleted_node->value);

        *top = (*top)->prev;
        free(deleted_node);
    }
}

int main() {
    Node *top_stack = NULL;

    for (int i = 1; i <= 100; i++) {
        push(&top_stack, i);
    }

    for (int i = 1; i <= 100; i++) {
        pop(&top_stack);
    }

    return 0;
}
