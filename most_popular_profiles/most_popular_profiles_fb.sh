#! /usr/bin/bash

set -e
export LC_ALL=C

find_popular_profiles() {(
	dataset_dir=$1
	profile=$2
	echo "find_popular_profiles $dataset_dir $profile"
	cd "$dataset_dir"
	mkdir -p "most_popular_profiles_table/profiles/$profile/"
	completed_list="most_popular_profiles_table/profiles/$profile/completed"
	touch "$completed_list"
	while read graph; do
		file="most_popular_profiles_table/profiles/$profile/${graph/%\.showg}"
		if [ -f "$file" ]; then
			if grep -qxf "$completed_list" <<< "$file"; then
				echo -e "\t$file already completed, skipping"
				continue
			else
				echo -e "\t$file is incomplete, rebuilding"
			fi
		fi
		echo -e "\t$profile: $graph"
		lines=$(grep '^Graph' "graphs_showg/$graph" | wc -l | cut -d ' ' -f 1)
		./programs/profiler/profiler neighborhood "$profile" "graphs_showg/$graph" --no-showg \
		| pv --buffer-size 512M --line-mode --size "$lines" | sort | uniq -c | sort -n -r \
		> "$file"
		exit_codes=("${PIPESTATUS[@]}")
		for code in "${exit_codes[@]}"; do
			if ! [ "$code" == '0' ]; then
				echo "error, profile: $profile, dataset_dir: $dataset_dir"
				echo "exit codes: ${exit_codes[@]}"
				exit 1
			fi
		done
		echo "$file" >> "$completed_list"
	done <<< "$(seq 2 "$VERTICES" | while read n; do printf "%02d_vertices.showg\n" "$n"; done)"
)}

if [ $# == 0 ]; then
	echo "args: n [dir in datasets...]"
	exit
fi

VERTICES=$1
shift

for dataset_dir in "$@"; do
	find_popular_profiles "$dataset_dir" Imax
	find_popular_profiles "$dataset_dir" Imin
	find_popular_profiles "$dataset_dir" Emax
	find_popular_profiles "$dataset_dir" Emin
	find_popular_profiles "$dataset_dir" Range
	find_popular_profiles "$dataset_dir" Id
	find_popular_profiles "$dataset_dir" Sum
	find_popular_profiles "$dataset_dir" Different
	find_popular_profiles "$dataset_dir" Popular
done
