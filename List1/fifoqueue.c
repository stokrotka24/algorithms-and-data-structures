#include <stdio.h>
#include <malloc.h>

typedef struct Elem {
    int value;
    struct Elem *next;
} Node;

typedef struct {
    Node *head;
    Node *tail;
} Queue;

int size(Queue *queue) {
    int size = 0;
    Node *node = queue->head;

    while (node != NULL) {
        size++;
        node = node->next;
    }
    return size;
}

int is_empty(Queue *queue) {
    return queue->head == NULL;
}

void push(Queue *queue, int val) {
    Node *new_node = malloc(sizeof(Node));
    new_node->value = val;
    new_node->next = NULL;

    if (is_empty(queue)) {
        queue->head = new_node;
    } else {
        queue->tail->next = new_node;
    }
    queue->tail = new_node;

    printf("Adding %d\n", val);
}

void pop(Queue *queue) {
    if (is_empty(queue)) {
        printf("Nothing to pop\n");
    } else {
        Node *deleted_Node = queue->head;
        printf("Popping %d\n", deleted_Node->value);

        queue->head = queue->head->next;
        free(deleted_Node);
    }
}

int main() {
    Queue queue = {.head = NULL, .tail = NULL};

    for (int i = 1; i <= 100; i++) {
        push(&queue, i);
    }

    for (int i = 1; i <= 100; i++) {
        pop(&queue);
    }

    return 0;
}
