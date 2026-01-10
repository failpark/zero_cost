#include <stdlib.h>
#include "filehandle_unsafe.h"

file_handle_t* file_handle_new() {
	file_handle_t* h = malloc(sizeof(file_handle_t));
	h->data = 0;
	return h;
}

void file_handle_open(file_handle_t* h) {
	// No state check, just do it
}

void file_handle_read(file_handle_t* h) {
	h->data = 42;
}

int file_handle_get_data(file_handle_t* h) {
	return h->data;
}

void file_handle_close(file_handle_t* h) {
	h->data = 0;
}

void file_handle_drop(file_handle_t* h) {
	free(h);
}
