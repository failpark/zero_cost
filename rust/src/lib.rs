use std::marker::PhantomData;

// Type-level state markers
pub struct Closed;
pub struct Open;
pub struct Readable;

// The FileHandle with zero-sized type parameter
#[repr(C)]
pub struct FileHandle<State> {
	data: i32,
	_state: PhantomData<State>,
}

// C-compatible exports for assembly comparison
// These use #[no_mangle] and extern "C" to prevent optimization

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn rust_file_handle_new() -> FileHandle<Closed> {
	FileHandle {
		data: 0,
		_state: PhantomData,
	}
}

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn rust_file_handle_open(_handle: FileHandle<Closed>) -> FileHandle<Open> {
	FileHandle {
		data: 0,
		_state: PhantomData,
	}
}

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn rust_file_handle_read(_handle: FileHandle<Open>) -> FileHandle<Readable> {
	FileHandle {
		data: 42,
		_state: PhantomData,
	}
}

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn rust_file_handle_get_data(handle: &FileHandle<Readable>) -> i32 {
	handle.data
}

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn rust_file_handle_close(_handle: FileHandle<Readable>) -> FileHandle<Closed> {
	FileHandle {
		data: 0,
		_state: PhantomData,
	}
}
