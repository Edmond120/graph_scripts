#! /usr/bin/bash

# this program requires showg from the nauty package

{ # error checking
	if [[ $# -lt 1 ]]; then
		echo 'usage: show_degree_sequence graph6_file'
		exit 1
	fi

	if  ! [[ -f $1 ]]; then
		echo "$1 is not a file"
		exit 1
	fi
} >&2

count_char() {
	local string=$1
	local char=$2
	local count=0
	for ((i = 0; i < ${#string}; i++)); do
		if [[ ${string:i:1} == $char ]]; then
			((count++))
		fi
	done
	echo "$count"
}

( showg -q "$1"; echo 0 ) | { # echo 0 is so that the loop prints the final sequence
	# first line from showg is useless
	read line
	degree_seq=()
	while read line; do
		if [[ $line =~ ^[0-9]+$ ]]; then
			data=$(echo "${degree_seq[@]}" | tr ' ' '\n' | sort | tr '\n' ' ')
			echo ${data:0:-1}
			degree_seq=()
		else
			degree_seq+=("$(count_char "${line#*:}" ' ')")
		fi
	done
}
