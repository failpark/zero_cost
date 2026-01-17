_default:
	@just --list

open:
	open paper/main.pdf
	open poster/main.pdf

fmt:
	cd rust && just fmt

check:
	cd rust && just clippy

compile: paper poster

paper:
	cd paper && just compile

poster:
	cd poster && just compile

metrics-out:
	python3 scripts/collect_metrics.py --skip-build -o scripts/metrics.csv

metrics: _compile_all _dump_all
	uv run paper/scripts/collect_metrics.py

_compile_all:
	cd c && just c
	cd rust && just c

_dump_all:
	cd c && just d
	cd rust && just d
