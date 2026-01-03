#include <stdio.h>
#include <stdlib.h>

typedef struct {
	int data;
} file_handle_t;  // No state field at all

file_handle_t* create_handle() {
	file_handle_t* h = malloc(sizeof(file_handle_t));
	h->data = 0;
	return h;
}

void open_file(file_handle_t* h) {
	// No state check, just do it
}

int read_file(file_handle_t* h) {
	h->data = 42;
	return h->data;
}

void close_file(file_handle_t* h) {
	h->data = 0;
}

void destroy_handle(file_handle_t* h) {
	free(h);
}