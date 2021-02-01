#! /usr/bin/bash

# this program requires to be in the same directory as show_degree_sequence.sh

path=$(dirname "$0")

{ # error checking
	if [[ $# -lt 1 ]]; then
		echo 'usage: count_unique_sequences.sh graph6_file_1 [graph6_file_2] [...]'
		exit 1
	fi
} >&2

while [ $# -gt 0 ]; do
	file=$1
	shift
	if ! [ -f "$file" ]; then
		echo "$file : error, not a file"
		continue
	fi
	uniq_sequences=$(bash "$path/show_degree_sequence.sh" "$file" | pv --line-mode | sort | uniq | wc -l)
	echo "$(basename "$file") : unique sequences = $uniq_sequences"
done
