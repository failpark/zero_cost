use std::marker::PhantomData;

struct Closed;
struct Open;
struct Readable;

struct FileHandle<State> {
	data: i32,
	_state: PhantomData<State>,
}

impl FileHandle<Closed> {
	#[inline(never)]
	fn new() -> Self {
		FileHandle {
			data: 0,
			_state: PhantomData,
		}
	}

	#[inline(never)]
	fn open(self) -> FileHandle<Open> {
		FileHandle {
			data: self.data,
			_state: PhantomData,
		}
	}
}

impl FileHandle<Open> {
	#[inline(never)]
	fn read(self) -> FileHandle<Readable> {
		FileHandle {
			data: 42,
			_state: PhantomData,
		}
	}
}

impl FileHandle<Readable> {
	#[inline(never)]
	fn get_data(&self) -> i32 {
		self.data
	}

	#[inline(never)]
	fn close(self) -> FileHandle<Closed> {
		FileHandle {
			data: 0,
			_state: PhantomData,
		}
	}
}

#[inline(never)]
pub fn use_file() -> i32 {
	let f = FileHandle::<Closed>::new();
	let f = f.open();
	let f = f.read();
	let data = f.get_data();
	let _f = f.close();
	data
}

fn main() {
	// use_file();
	let f = FileHandle::<Closed>::new();
	let f = f.open();
	let f = f.read();
	let data = f.get_data();
	let _f = f.close();
	println!("{data}");
}
