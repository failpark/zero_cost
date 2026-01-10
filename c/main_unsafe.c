#include <stdio.h>
#include "filehandle_unsafe.h"

int main() {
	file_handle_t* f = file_handle_new();
	file_handle_open(f);
	file_handle_read(f);
	int data = file_handle_get_data(f);
	file_handle_close(f);
	file_handle_drop(f);
	printf("%d\n", data);
	return 0;
}
