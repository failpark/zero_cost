#!/usr/bin/env python3
"""Generate overhead ratio graph comparing Defensive C to Rust."""

import csv
import matplotlib.pyplot as plt
from pathlib import Path

# Set up paths
script_dir = Path(__file__).parent
data_file = script_dir / 'metrics.csv'
output_dir = script_dir.parent / 'paper' / 'figures'
output_file = output_dir / 'overhead_ratio.pdf'

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Read metrics from CSV
defensive_data = {}
rust_data = {}

with open(data_file, 'r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		func = row['function']
		total = int(row['total'])

		if row['implementation'] == 'defensive_c':
			defensive_data[func] = total
		elif row['implementation'] == 'rust':
			rust_data[func] = total

# Calculate overhead percentage: ((defensive - rust) / rust) * 100
functions = []
overhead_values = []

function_names = {
	'file_handle_get_data': 'get_data',
	'file_handle_open': 'open',
	'file_handle_read': 'read',
	'file_handle_close': 'close'
}

for func in sorted(defensive_data.keys()):
	if func in rust_data:
		defensive_total = defensive_data[func]
		rust_total = rust_data[func]
		overhead_pct = ((defensive_total - rust_total) / rust_total) * 100

		display_name = function_names.get(func, func)
		functions.append(display_name)
		overhead_values.append(overhead_pct)

# Create figure with IEEE-style formatting
fig, ax = plt.subplots(figsize=(7, 4))

# Create bar chart
bars = ax.bar(functions, overhead_values,
               color='#d62728', edgecolor='black', linewidth=1.2, alpha=0.8)

# Add value labels on top of bars
for bar in bars:
	height = bar.get_height()
	ax.text(bar.get_x() + bar.get_width()/2., height,
	        f'{height:.1f}%',
	        ha='center', va='bottom', fontsize=10, fontweight='bold')

# Formatting
ax.set_ylabel('Overhead (%)', fontsize=11, fontweight='bold')
ax.set_xlabel('Function', fontsize=11, fontweight='bold')
ax.set_title('Runtime Overhead: Defensive C vs Rust Typestate\n(Higher = More Overhead)',
             fontsize=12, fontweight='bold', pad=15)

# Grid for readability
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Y-axis starts at 0
ax.set_ylim(bottom=0, top=max(overhead_values) * 1.15)

# Tighten layout
plt.tight_layout()

# Save
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Overhead ratio graph saved to: {output_file}")

# Also display summary statistics
min_overhead = min(overhead_values)
max_overhead = max(overhead_values)
avg_overhead = sum(overhead_values) / len(overhead_values)
min_func = functions[overhead_values.index(min_overhead)]
max_func = functions[overhead_values.index(max_overhead)]

print("\nOverhead Summary:")
print(f"  Minimum: {min_overhead:.1f}% ({min_func})")
print(f"  Maximum: {max_overhead:.1f}% ({max_func})")
print(f"  Average: {avg_overhead:.1f}%")
print(f"\nDefensive C requires {avg_overhead:.1f}% more instructions on average.")
