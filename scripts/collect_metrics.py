#!/usr/bin/env python3
"""Collect assembly metrics for zero-cost abstraction comparison."""

import subprocess
import re
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Architecture-specific instruction patterns
ARM64_PATTERNS = {
	'branch': r'\b(b\.eq|b\.ne|b\.lt|b\.gt|b\.le|b\.ge|b\.lo|b\.hi|cbz|cbnz|tbz|tbnz)\b',
	'compare': r'\b(cmp|cmn|tst)\b',
	'memory': r'\b(ldr|str|ldp|stp|ldrb|strb|ldrh|strh|ldur|stur)\b',
	'arithmetic': r'\b(add|sub|mul|mov|and|orr|eor|adrp|neg|mvn)\b',
	'control': r'\b(ret|bl|br|blr)\b',
}

X86_PATTERNS = {
	'branch': r'\b(je|jne|jz|jnz|jl|jg|jle|jge|ja|jb|jae|jbe|jmp)\b',
	'compare': r'\b(cmp|test)\b',
	'memory': r'\b(mov.*\[|lea|push|pop)\b',
	'arithmetic': r'\b(add|sub|imul|mul|and|or|xor|neg|inc|dec)\b',
	'control': r'\b(ret|call)\b',
}

def detect_architecture() -> Dict[str, str]:
	"""Detect the architecture and return appropriate patterns."""
	result = subprocess.run(['uname', '-m'], capture_output=True, text=True)
	arch = result.stdout.strip()

	if arch in ['arm64', 'aarch64']:
		return ARM64_PATTERNS
	else:
		return X86_PATTERNS

def extract_function_asm(asm_text: str, func_name: str) -> List[str]:
	"""Extract assembly instructions for a specific function."""
	lines = asm_text.split('\n')
	in_function = False
	function_lines = []

	# Handle both C and Rust name formats
	# C: <_file_handle_get_data>:
	# Rust: may have mangled names
	pattern = f'<[^>]*{func_name}[^>]*>:'

	for line in lines:
		# Check if we're entering the target function
		if re.search(pattern, line):
			in_function = True
			continue

		# Check if we've hit the next function (new label)
		if in_function and re.match(r'^[0-9a-f]+\s+<[^>]+>:', line):
			break

		# Collect instruction lines (format: "  addr: hex  mnemonic operands")
		if in_function:
			# Match lines with hex address, colon, hex machine code, and instruction
			if re.match(r'^\s+[0-9a-f]+:\s+[0-9a-f]+\s+\w+', line):
				function_lines.append(line.strip())

	return function_lines

def count_instructions(asm_lines: List[str], patterns: Dict[str, str]) -> Dict[str, int]:
	"""Count instructions by category."""
	counts = {'total': len(asm_lines)}

	# Initialize all categories to 0
	for category in patterns.keys():
		counts[category] = 0

	# Count each category
	for line in asm_lines:
		# Extract just the mnemonic (instruction name)
		# Format: "addr: hex  mnemonic  operands"
		match = re.search(r':\s+[0-9a-f]+\s+(\w+\.?\w*)', line)
		if match:
			mnemonic = match.group(1)
			# Check each category
			for category, pattern in patterns.items():
				if re.search(pattern, mnemonic, re.IGNORECASE):
					counts[category] += 1
					# Don't break - some instructions might fit multiple categories

	return counts

def build_all():
	"""Build all implementations and extract assembly."""
	print("Building all implementations...", file=sys.stderr)

	root = Path('/Users/phedias/code/sem3/zero_cost')
	c_dir = root / 'c'
	rust_dir = root / 'rust'
	out_dir = c_dir / 'out'

	# Ensure output directory exists
	out_dir.mkdir(exist_ok=True)

	# Build defensive C
	print("  Building defensive C...", file=sys.stderr)
	subprocess.run(
		['gcc', '-O2', '-c', 'filehandle.c', '-o', 'out/filehandle.o'],
		cwd=c_dir, check=True
	)
	subprocess.run(
		['objdump', '-d', 'out/filehandle.o'],
		cwd=c_dir, capture_output=True, text=True, check=True
	).stdout
	subprocess.run(
		['sh', '-c', 'objdump -d out/filehandle.o > out/filehandle_asm.txt'],
		cwd=c_dir, check=True
	)

	# Build minimal C
	print("  Building minimal C...", file=sys.stderr)
	subprocess.run(
		['gcc', '-O2', '-c', 'filehandle_unsafe.c', '-o', 'out/filehandle_unsafe.o'],
		cwd=c_dir, check=True
	)
	subprocess.run(
		['sh', '-c', 'objdump -d out/filehandle_unsafe.o > out/filehandle_unsafe_asm.txt'],
		cwd=c_dir, check=True
	)

	# Build Rust (as cdylib to prevent whole-program optimization)
	print("  Building Rust library...", file=sys.stderr)
	subprocess.run(
		['cargo', 'build', '--release', '--lib'],
		cwd=rust_dir, check=True, capture_output=True
	)
	subprocess.run(
		['sh', '-c', 'objdump -d target/release/libfilehandle.dylib > ../c/out/rust_asm.txt'],
		cwd=rust_dir, check=True
	)

	print("Build complete!", file=sys.stderr)

def analyze_all_functions():
	"""Analyze all implementations and output CSV."""
	patterns = detect_architecture()
	arch_name = "ARM64" if patterns == ARM64_PATTERNS else "x86_64"
	print(f"Detected architecture: {arch_name}", file=sys.stderr)

	c_dir = Path('/Users/phedias/code/sem3/zero_cost/c')

	# Read assembly files
	defensive_asm = (c_dir / 'out/filehandle_asm.txt').read_text()
	minimal_asm = (c_dir / 'out/filehandle_unsafe_asm.txt').read_text()
	rust_asm = (c_dir / 'out/rust_asm.txt').read_text()

	# Functions to analyze
	functions = [
		'file_handle_get_data',
		'file_handle_open',
		'file_handle_read',
		'file_handle_close',
	]

	results = []

	# Analyze each implementation
	for func in functions:
		# Defensive C
		c_func = f'_file_handle_{func.replace("file_handle_", "")}'
		asm_lines = extract_function_asm(defensive_asm, c_func)
		if asm_lines:
			counts = count_instructions(asm_lines, patterns)
			results.append({
				'implementation': 'defensive_c',
				'function': func,
				**counts
			})

		# Minimal C
		asm_lines = extract_function_asm(minimal_asm, c_func)
		if asm_lines:
			counts = count_instructions(asm_lines, patterns)
			results.append({
				'implementation': 'minimal_c',
				'function': func,
				**counts
			})

		# Rust (cdylib exports with rust_file_handle_ prefix)
		rust_func = f'_rust_{func}'
		asm_lines = extract_function_asm(rust_asm, rust_func)
		if asm_lines:
			counts = count_instructions(asm_lines, patterns)
			results.append({
				'implementation': 'rust',
				'function': func,
				**counts
			})

	return results

def main():
	"""Main entry point."""
	import argparse

	parser = argparse.ArgumentParser(
		description='Collect assembly metrics for zero-cost abstraction comparison'
	)
	parser.add_argument(
		'--skip-build',
		action='store_true',
		help='Skip building and use existing assembly files'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		default=None,
		help='Output CSV file (default: stdout)'
	)

	args = parser.parse_args()

	# Build if needed
	if not args.skip_build:
		build_all()

	# Analyze
	print("\nAnalyzing assembly...", file=sys.stderr)
	results = analyze_all_functions()

	# Output CSV
	if results:
		fieldnames = ['implementation', 'function', 'total', 'branch', 'compare',
		              'memory', 'arithmetic', 'control']

		output_file = sys.stdout
		if args.output:
			output_file = open(args.output, 'w')

		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()
		for row in results:
			writer.writerow(row)

		if args.output:
			output_file.close()
			print(f"\nMetrics written to {args.output}", file=sys.stderr)
	else:
		print("No results found!", file=sys.stderr)
		return 1

	return 0

if __name__ == '__main__':
	sys.exit(main())
