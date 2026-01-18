#!/usr/bin/env python3
"""Generate visualization graphs for zero-cost abstractions paper."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Output directory
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Color scheme
COLORS = {
	'defensive': '#ff6b6b',  # Red - has overhead
	'minimal': '#4ecdc4',    # Teal - baseline
	'rust': '#f7931e',       # Orange - highlight
}

def graph1_instruction_count():
	"""Bar chart: Total instruction count comparison."""
	implementations = ['Defensive C', 'Minimal C', 'Rust']
	instructions = [9, 2, 2]
	colors = [COLORS['defensive'], COLORS['minimal'], COLORS['rust']]

	_fig, ax = plt.subplots(figsize=(6, 4))
	bars = ax.bar(implementations, instructions, color=colors, edgecolor='black', linewidth=0.5)

	# Add value labels on bars
	for bar, val in zip(bars, instructions):
		ax.text(
			bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
			str(val), ha='center', va='bottom', fontweight='bold'
		)

	ax.set_ylabel('Instruction Count')
	# ax.set_title('Assembly Instructions at -O2 (file_handle_get_data)')
	ax.set_ylim(0, 9)
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)

	plt.tight_layout()
	# plt.savefig(FIGURES_DIR / 'instruction_count.pdf', bbox_inches='tight')
	plt.savefig(FIGURES_DIR / 'instruction_count_without_title.svg')
	plt.close()
	print(f"✓ Generated {FIGURES_DIR / 'instruction_count.pdf'}")

def graph2_instruction_breakdown():
	"""Grouped bar chart: Instruction category breakdown."""
	categories = ['Memory', 'Branches', 'Arithmetic', 'Call/Ret']

	defensive_c = [2, 1, 4, 2]  # Total: 9
	minimal_c = [0, 0, 1, 1]    # Total: 2
	rust = [0, 0, 1, 1]         # Total: 2

	x = np.arange(len(categories))
	width = 0.25

	_fig, ax = plt.subplots(figsize=(8, 5))

	ax.bar(x - width, defensive_c, width, label='Defensive C',
		color=COLORS['defensive'], edgecolor='black', linewidth=0.5)
	ax.bar(x, minimal_c, width, label='Minimal C',
		color=COLORS['minimal'], edgecolor='black', linewidth=0.5)
	ax.bar(x + width, rust, width, label='Rust',
		color=COLORS['rust'], edgecolor='black', linewidth=0.5)

	ax.set_ylabel('Instruction Count')
	# ax.set_title('Instruction Categories by Implementation')
	ax.set_xticks(x)
	ax.set_xticklabels(categories)
	ax.legend()
	ax.set_ylim(0, 3)
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)

	# Highlight the key finding: Rust has 0 branches
	# ax.annotate(
		# 'Zero branches\n(compile-time safety)',
		# xy=(1 + width, 0), xytext=(1.5, 1.5),
		# arrowprops=dict(arrowstyle='->', color='gray'),
		# fontsize=9, ha='center'
	# )

	plt.tight_layout()
	# plt.savefig(FIGURES_DIR / 'instruction_breakdown.pdf', bbox_inches='tight')
	plt.savefig(FIGURES_DIR / 'instruction_breakdown_without_title.svg')
	plt.close()
	print(f"✓ Generated {FIGURES_DIR / 'instruction_breakdown.pdf'}")

if __name__ == '__main__':
	print("Generating graphs for zero-cost abstractions paper...")
	graph1_instruction_count()
	graph2_instruction_breakdown()
	print(f"\n✓ All graphs saved to {FIGURES_DIR}")
