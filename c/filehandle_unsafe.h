#ifndef FILEHANDLE_UNSAFE_H
#define FILEHANDLE_UNSAFE_H

typedef struct {
	int data;
} file_handle_t;

file_handle_t* file_handle_new();
void file_handle_open(file_handle_t* h);
void file_handle_read(file_handle_t* h);
int file_handle_get_data(file_handle_t* h);
void file_handle_close(file_handle_t* h);
void file_handle_drop(file_handle_t* h);

#endif
