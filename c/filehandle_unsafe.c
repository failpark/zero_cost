#include <stdlib.h>
#include "filehandle.h"

file_handle_t* file_handle_new() {
	file_handle_t* h = malloc(sizeof(file_handle_t));
	h->data = 0;
	return h;
}

// Returns 0 on success, -1 on invalid state
int file_handle_open(file_handle_t* h) {
	// No state check, just do it
	return 0;
}

int file_handle_read(file_handle_t* h) {
	h->data = 42;
	return 0;
}

int file_handle_get_data(file_handle_t* h) {
	return h->data;
}

int file_handle_close(file_handle_t* h) {
	h->data = 0;
	return 0;
}

void file_handle_drop(file_handle_t* h) {
	free(h);
}
