#! /usr/bin/bash

export LC_ALL=C

find_popular_profiles() {(
	dataset_dir=$1
	profile=$2
	echo "find_popular_profiles $dataset_dir $profile"
	cd "$dataset_dir"
	mkdir -p "most_popular_profiles_table/$profile/"
	while read graph; do
		file="most_popular_profiles_table/$profile/${graph/%\.showg}"
		if [ -f "$file" ]; then
			echo -e "\t$file already exist, skipping"
			read -p 'press enter to continue... ' < /dev/tty
			continue
		fi
		echo -e "\t$graph"
		lines=$(wc -l "graphs_showg/$graph" | cut -d ' ' -f 1)
		./programs/profiler/profiler \
			neighborhood "$profile" "graphs_showg/$graph" --no-showg \
			| pv --buffer-size 512M --line-mode --size "$lines" | sort | uniq -c | sort -n -r \
			> "$file"
	done <<< "$(ls graphs_showg)"
)}

if [ $# == 0 ]; then
	echo "args: [dir in datasets...]"
	exit
fi

for dataset_dir in "$@"; do
	find_popular_profiles "$dataset_dir" Imax
	find_popular_profiles "$dataset_dir" Imin
	find_popular_profiles "$dataset_dir" Emax
	find_popular_profiles "$dataset_dir" Emin
	find_popular_profiles "$dataset_dir" Range
	find_popular_profiles "$dataset_dir" Id
	find_popular_profiles "$dataset_dir" Sum
done
