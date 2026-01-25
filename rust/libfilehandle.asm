
./target/release/libfilehandle.dylib:	file format mach-o arm64

Disassembly of section __TEXT,__text:

0000000000000330 <_rust_file_handle_open>:
     330: d2800000     	mov	x0, #0x0                ; =0
     334: d65f03c0     	ret

0000000000000338 <_rust_file_handle_get_data>:
     338: b9400000     	ldr	w0, [x0]
     33c: d65f03c0     	ret

0000000000000340 <_rust_file_handle_new>:
     340: d2800000     	mov	x0, #0x0                ; =0
     344: d65f03c0     	ret

0000000000000348 <_rust_file_handle_read>:
     348: 52800540     	mov	w0, #0x2a               ; =42
     34c: d65f03c0     	ret
