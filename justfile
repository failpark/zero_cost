_default:
	@just --list

open:
	open paper/main.pdf
	open poster/main.pdf

fmt:
	cd rust && just fmt

check:
	cd rust && just clippy

compile-paper:
	cd paper && just compile
	# cd c && just build
	# cd rust && just asm-release

compile-poster:
	cd poster && just compile

metrics-out:
	python3 scripts/collect_metrics.py --skip-build -o scripts/metrics.csv

metrics:
	python3 scripts/collect_metrics.py
