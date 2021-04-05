#! /usr/bin/bash

set -e
scripts=$(dirname "$BASH_SOURCE")
scripts=$(realpath "$scripts")

make_table() {(
	cd "$1"
	cd most_popular_profiles_table
	mkdir -p tables
	cd profiles
	for profile in *; do
		show_profile "$profile" \
			> "../tables/$profile"
	done
	cd ../tables
	if [ -f table.txt ]; then
		rm table.txt
	fi
	n=$(wc -l "$(ls | head -n 1)" | cut -d ' ' -f 1)
	((n=n+1))
	paste <(seq 2 "$n") * | column -t -N "n,$(echo -n * | tr ' ' ',')" \
		| tee table.txt
)}

show_profile() {(
	cd "$1"
	for file in *_vertices; do
		python "$scripts/tie_breaker.py" "$file"
	done
)}

for dir in "$@"; do
	make_table "$dir"
done
