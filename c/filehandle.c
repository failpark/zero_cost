#include <stdlib.h>
#include "filehandle.h"

file_handle_t* file_handle_new() {
	file_handle_t* h = malloc(sizeof(file_handle_t));
	h->state = STATE_CLOSED;
	h->data = 0;
	return h;
}

// Returns 0 on success, -1 on invalid state
int file_handle_open(file_handle_t* h) {
	if (h->state != STATE_CLOSED) {
		return -1;  // Invalid state transition
	}
	h->state = STATE_OPEN;
	return 0;
}

int file_handle_read(file_handle_t* h) {
	if (h->state != STATE_OPEN) {
		return -1;  // Invalid state transition
	}
	h->state = STATE_READABLE;
	h->data = 42;  // Simulate reading data
	return 0;
}

int file_handle_get_data(file_handle_t* h) {
	if (h->state != STATE_READABLE) {
		return -1;  // Can only get data when readable
	}
	return h->data;
}

int file_handle_close(file_handle_t* h) {
	if (h->state == STATE_CLOSED) {
		return -1;  // Already closed
	}
	h->state = STATE_CLOSED;
	h->data = 0;
	return 0;
}

void file_handle_drop(file_handle_t* h) {
	free(h);
}
