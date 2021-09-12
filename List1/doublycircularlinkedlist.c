#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NO_TESTS 500
#define NO_TEST_VALUES 5
#define NO_NODES 1000

typedef struct Elem {
    int value;
    struct Elem *prev;
    struct Elem *next;
} Node;

int list_is_empty(Node *head) {
    return head == NULL;
}

void print_list(Node *head) {
    int size = 0;

    if (!list_is_empty(head)) {
        Node *tmp = head;

        /*At first tmp = head, so it must be do-while*/
        do {
            printf("%d ", tmp->value);
            size++;
            tmp = tmp->next;
        } while (tmp != head);
    }
    printf("\nSize: %d\n", size);
}

void add_node(Node **head, int val) {
    Node *new_node = malloc(sizeof(Node));
    new_node->value = val;

    if (list_is_empty(*head)) {
        new_node->prev = new_node;
        new_node->next = new_node;
        *head = new_node;
    } else {
        new_node->prev = (*head)->prev;
        (*head)->prev->next = new_node;
        (*head)->prev = new_node;
        new_node->next = *head;
    }

//    printf("Adding %d\n", val);
}

int find(Node *head, int val) {
    int nodes = 0;

    if (!list_is_empty(head)) {
        Node *tmp = head;

        do {
            if (tmp->value == val) {
                return nodes;
            }
            nodes++;
            tmp = tmp->next;
        } while (tmp != head);
    }
    return -1;
}

void delete_node(Node **head, int val) {
    if (list_is_empty(*head)) {
        printf("Nothing to delete\n");
    } else {
        Node *tmp = *head;
        Node *tail = (*head)->prev;
        Node *prev_node, *next_node;
        int deleted = 0;

        while (tmp != tail) {
            if (tmp->value == val) {
                deleted = 1;

                prev_node = tmp->prev;
                next_node = tmp->next;
                prev_node->next = next_node;
                next_node->prev = prev_node;

                /* First node */
                if (tmp == *head) {
                    *head = (*head)->next;
                }

                free(tmp);
                tmp = next_node;
            } else {
                tmp = tmp->next;
            }
        }

        if(tail->value == val) {
            deleted = 1;

            if (*head == tail) {
                (*head) = NULL;

            } else {
                prev_node = tmp->prev;
                prev_node->next = *head;
                (*head)->prev = prev_node;
            }
            free(tmp);
        }

        if (deleted == 0) {
            printf("There is no value %d\n", val);
        }
    }
}


void delete_list(Node **head) {
    if(!list_is_empty(*head)) {
        Node *tmp = *head;
        Node *tail = (*head)->prev;
        Node *prev_node, *next_node;

        do {
            prev_node = tmp->prev;
            next_node = tmp->next;

            prev_node->next = next_node;
            next_node->prev = prev_node;

            *head = (*head)->next;

            free(tmp);
            tmp = next_node;
        } while (tmp != tail);

        (*head) = NULL;
        free(tmp);
    }
}


void merge(Node** head1, Node** head2) {
    if (list_is_empty(*head1) && list_is_empty(*head2)) {
        printf("Merging two empty lists is impossible\n");
    } else {
        (*head1)->prev->next = *head2;
        (*head2)->prev->next = *head1;

        Node *tmp = (*head1)->prev;
        (*head1)->prev = (*head2)->prev;
        (*head2)->prev = tmp;
    }
}

void shuffle_array(int *array) {
    for (int i = 0; i < NO_NODES; i++) {
        int num = (int) (random() % NO_NODES);
        int tmp = array[i];
        array[i] = array[num];
        array[num] = tmp;
    }
}

void access_test(int *values, int *tested_vals, int *num_nodes) {
    for (int i = 0; i < NO_TESTS; i++) {
        Node *head = NULL;
        shuffle_array(values);

        for (int k = 0; k < NO_NODES; k++) {
            add_node(&head, values[k]);
        }

        for (int j = 0; j < NO_TEST_VALUES; j++) {
            num_nodes[j] += find(head, tested_vals[j]);
        }

        delete_list(&head);
    }

    for (int i = 0; i < NO_TEST_VALUES - 1; i++) {
        num_nodes[i] = num_nodes[i] / NO_TESTS;
        printf("Average access time to const value = %d is %d nodes\n", tested_vals[i], num_nodes[i]);
    }

    num_nodes[NO_TEST_VALUES - 1] = num_nodes[NO_TEST_VALUES - 1] / NO_TESTS;
    printf("Average access time to random value = %d is %d nodes\n", tested_vals[NO_TEST_VALUES - 1], num_nodes[NO_TEST_VALUES - 1]);
}

int main() {
    srandom(time(NULL));

    int *values = malloc(NO_NODES * sizeof(int));
    for (int i = 0; i < NO_NODES; i++) {
        values[i] = i + 1;
    }

    int random_value = ((int) (random() % NO_NODES)) + 1;
    int tested_vals[NO_TEST_VALUES] = {35, 62, 333, 901, random_value};
    int num_nodes[NO_TEST_VALUES] = {0, 0, 0, 0, 0};
    access_test(values, tested_vals, num_nodes);

    Node *head1 = NULL;
    shuffle_array(values);

    for (int i = 0; i < NO_NODES; i++) {
        add_node(&head1, values[i]);
    }

    printf("\n");

    Node *head2 = NULL;
    shuffle_array(values);

    for (int i = 0; i < NO_NODES; i++) {
        add_node(&head2, values[i]);
    }

    print_list(head1);
    print_list(head2);
    merge(&head1, &head2);
    print_list(head1);
    printf("%d\n", find(head1,2));
    delete_node(&head1, 2);
    printf("%d\n", find(head1,2));

    free(values);
    delete_list(&head1);
    print_list(head1);
    return 0;
}
