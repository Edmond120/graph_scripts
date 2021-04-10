#! /usr/bin/bash

set -e
scripts=$(dirname "$BASH_SOURCE")
scripts=$(realpath "$scripts")

make_table() {(
	cd "$1"
	prefix=$2
	table_name=$3
	cd most_popular_profiles_table
	mkdir -p tables
	cd profiles
	for profile in "$prefix"*; do
		show_profile "$profile" \
			> "../tables/$profile"
	done
	cd ../tables
	if [ -f "$table_name" ]; then
		rm "$table_name"
	fi
	n=$(wc -l "$(find -type f ! -name '*.txt' | head -n 1)" | cut -d ' ' -f 1)
	((n=n+1))
	paste <(seq 2 "$n") "$prefix"* | column -t -N "n,$(echo -n "$prefix"* | tr ' ' ',')" \
		| tee "$table_name"
)}

show_profile() {(
	cd "$1"
	for file in *_vertices; do
		python "$scripts/tie_breaker.py" "$file"
	done
)}

for dir in "$@"; do
	make_table "$dir" I inclusive_table.txt
	make_table "$dir" E exclusive_table.txt
done
