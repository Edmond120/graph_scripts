#! /usr/bin/python
import sys

count_table = {}

for line in sys.stdin:
	line = line[:-1]
	if line in count_table:
		count_table[line] += 1
	else:
		count_table[line] = 1

max_int_length = max(map(lambda v: len(str(v)), count_table.values()))

if len(sys.argv) > 1 and sys.argv[1] == '--sort':
	order = list(count_table.keys())
	order.sort(key=lambda k: count_table[k], reverse=True)
else:
	order = count_table.keys()

for key in order:
	padding = max_int_length - len(str(count_table[key]))
	print(f' {" " * padding}{count_table[key]} {key}')
