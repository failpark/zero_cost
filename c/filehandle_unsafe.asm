
out/filehandle_unsafe.o:	file format mach-o arm64

Disassembly of section __TEXT,__text:

0000000000000000 <ltmp0>:
       0: a9bf7bfd     	stp	x29, x30, [sp, #-0x10]!
       4: 910003fd     	mov	x29, sp
       8: 52800100     	mov	w0, #0x8                ; =8
       c: 94000000     	bl	0xc <ltmp0+0xc>
      10: b900041f     	str	wzr, [x0, #0x4]
      14: a8c17bfd     	ldp	x29, x30, [sp], #0x10
      18: d65f03c0     	ret

000000000000001c <_file_handle_open>:
      1c: 52800000     	mov	w0, #0x0                ; =0
      20: d65f03c0     	ret

0000000000000024 <_file_handle_read>:
      24: 52800548     	mov	w8, #0x2a               ; =42
      28: b9000408     	str	w8, [x0, #0x4]
      2c: 52800000     	mov	w0, #0x0                ; =0
      30: d65f03c0     	ret

0000000000000034 <_file_handle_get_data>:
      34: b9400400     	ldr	w0, [x0, #0x4]
      38: d65f03c0     	ret

000000000000003c <_file_handle_close>:
      3c: b900041f     	str	wzr, [x0, #0x4]
      40: 52800000     	mov	w0, #0x0                ; =0
      44: d65f03c0     	ret

0000000000000048 <_file_handle_drop>:
      48: 14000000     	b	0x48 <_file_handle_drop>
