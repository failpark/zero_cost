
out/filehandle.o:	file format mach-o arm64

Disassembly of section __TEXT,__text:

0000000000000000 <ltmp0>:
       0: a9bf7bfd     	stp	x29, x30, [sp, #-0x10]!
       4: 910003fd     	mov	x29, sp
       8: 52800100     	mov	w0, #0x8                ; =8
       c: 94000000     	bl	0xc <ltmp0+0xc>
      10: f900001f     	str	xzr, [x0]
      14: a8c17bfd     	ldp	x29, x30, [sp], #0x10
      18: d65f03c0     	ret

000000000000001c <_file_handle_open>:
      1c: b9400009     	ldr	w9, [x0]
      20: 34000069     	cbz	w9, 0x2c <_file_handle_open+0x10>
      24: 12800000     	mov	w0, #-0x1               ; =-1
      28: d65f03c0     	ret
      2c: aa0003e8     	mov	x8, x0
      30: 52800000     	mov	w0, #0x0                ; =0
      34: 52800029     	mov	w9, #0x1                ; =1
      38: b9000109     	str	w9, [x8]
      3c: d65f03c0     	ret

0000000000000040 <_file_handle_read>:
      40: b9400009     	ldr	w9, [x0]
      44: 7100053f     	cmp	w9, #0x1
      48: 540000e1     	b.ne	0x64 <_file_handle_read+0x24>
      4c: aa0003e8     	mov	x8, x0
      50: 52800000     	mov	w0, #0x0                ; =0
      54: 90000009     	adrp	x9, 0x0 <ltmp0>
      58: fd400120     	ldr	d0, [x9]
      5c: fd000100     	str	d0, [x8]
      60: d65f03c0     	ret
      64: 12800000     	mov	w0, #-0x1               ; =-1
      68: d65f03c0     	ret

000000000000006c <_file_handle_get_data>:
      6c: b9400008     	ldr	w8, [x0]
      70: 7100091f     	cmp	w8, #0x2
      74: 54000061     	b.ne	0x80 <_file_handle_get_data+0x14>
      78: b9400400     	ldr	w0, [x0, #0x4]
      7c: d65f03c0     	ret
      80: 12800000     	mov	w0, #-0x1               ; =-1
      84: d65f03c0     	ret

0000000000000088 <_file_handle_close>:
      88: b9400009     	ldr	w9, [x0]
      8c: 340000a9     	cbz	w9, 0xa0 <_file_handle_close+0x18>
      90: aa0003e8     	mov	x8, x0
      94: 52800000     	mov	w0, #0x0                ; =0
      98: f900011f     	str	xzr, [x8]
      9c: d65f03c0     	ret
      a0: 12800000     	mov	w0, #-0x1               ; =-1
      a4: d65f03c0     	ret

00000000000000a8 <_file_handle_drop>:
      a8: 14000000     	b	0xa8 <_file_handle_drop>
