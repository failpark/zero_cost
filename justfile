_default:
	@just --list

fmt:
	cd rust && just fmt

check:
	cd rust && just clippy
