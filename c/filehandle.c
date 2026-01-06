#include <stdio.h>
#include <stdlib.h>

typedef enum {
	STATE_CLOSED,
	STATE_OPEN,
	STATE_READABLE
} state_t;

typedef struct {
	state_t state;
	int data;
} file_handle_t;

file_handle_t* create_handle() {
	file_handle_t* h = malloc(sizeof(file_handle_t));
	h->state = STATE_CLOSED;
	h->data = 0;
	return h;
}

// Returns 0 on success, -1 on invalid state
int open_file(file_handle_t* h) {
	if (h->state != STATE_CLOSED) {
		return -1;  // Invalid state transition
	}
	h->state = STATE_OPEN;
	return 0;
}

int read_file(file_handle_t* h) {
	if (h->state != STATE_OPEN) {
		return -1;  // Invalid state transition
	}
	h->state = STATE_READABLE;
	h->data = 42;  // Simulate reading data
	return h->data;
}

int close_file(file_handle_t* h) {
	if (h->state == STATE_CLOSED) {
		return -1;  // Already closed
	}
	h->state = STATE_CLOSED;
	h->data = 0;
	return 0;
}

void destroy_handle(file_handle_t* h) {
	free(h);
}

int main(){
	return 0;
}
