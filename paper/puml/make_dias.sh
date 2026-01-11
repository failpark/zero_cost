#!/bin/bash

for f in $(find . -type f -maxdepth 1 -name "*.puml"); do
	plantuml $f -png &
	plantuml $f -svg &
done

exit 0
