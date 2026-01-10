#ifndef FILEHANDLE_H
#define FILEHANDLE_H

typedef enum {
	STATE_CLOSED,
	STATE_OPEN,
	STATE_READABLE
} state_t;

typedef struct {
	state_t state;
	int data;
} file_handle_t;

file_handle_t* file_handle_new();
int file_handle_open(file_handle_t* h);
int file_handle_read(file_handle_t* h);
int file_handle_get_data(file_handle_t* h);
int file_handle_close(file_handle_t* h);
void file_handle_drop(file_handle_t* h);

#endif
