#! /usr/bin/bash

set -e
export LC_ALL=C

find_popular_profiles() {(
	dataset_dir=$1
	neighborhood_type=$2
	profile=$3
	dirname=$4
	echo "find_popular_profiles $dataset_dir $dirname"
	cd "$dataset_dir"
	mkdir -p "most_popular_profiles_table/profiles/$dirname/"
	completed_list="most_popular_profiles_table/profiles/$dirname/completed"
	touch "$completed_list"
	while read graph; do
		file="most_popular_profiles_table/profiles/$dirname/${graph/%\.showg}"
		if [ -f "$file" ]; then
			if grep -qxf "$completed_list" <<< "$file"; then
				echo -e "\t$file already completed, skipping"
				continue
			else
				echo -e "\t$file is incomplete, rebuilding"
			fi
		fi
		echo -e "\t$dirname: $graph"
		lines=$(grep '^Graph' "graphs_showg/$graph" | wc -l | cut -d ' ' -f 1)
		./programs/profiler/profiler neighborhood "$neighborhood_type" "$profile" "graphs_showg/$graph" --no-showg \
		| pv --buffer-size 512M --line-mode --size "$lines" | sort | uniq -c | sort -n -r \
		> "$file"
		exit_codes=("${PIPESTATUS[@]}")
		for code in "${exit_codes[@]}"; do
			if ! [ "$code" == '0' ]; then
				echo "error, dirname: $dirname, dataset_dir: $dataset_dir"
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
	find_popular_profiles "$dataset_dir" inclusive Max Imax
	find_popular_profiles "$dataset_dir" exclusive Max Emax
	find_popular_profiles "$dataset_dir" inclusive Min Imin
	find_popular_profiles "$dataset_dir" exclusive Min Emin
	find_popular_profiles "$dataset_dir" inclusive Range Irange
	find_popular_profiles "$dataset_dir" exclusive Range Erange
	find_popular_profiles "$dataset_dir" inclusive Sum Isum
	find_popular_profiles "$dataset_dir" exclusive Sum Esum
	find_popular_profiles "$dataset_dir" inclusive Different Idifferent
	find_popular_profiles "$dataset_dir" exclusive Different Edifferent
	find_popular_profiles "$dataset_dir" inclusive Popular Ipopular
	find_popular_profiles "$dataset_dir" exclusive Popular Epopular
done
