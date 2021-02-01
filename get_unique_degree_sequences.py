#! /usr/bin/python

import subprocess
import sys

def get_unique_degree_sequences(file_):
	with subprocess.Popen(['showg', '-q', file_], stdout=subprocess.PIPE).stdout as pipe:
		uniq_sequences = set()
		degree_seq = []
		for line in pipe:
			line = line.decode('utf-8')
			if line.count(':') == 0:
				if len(degree_seq) > 0:
					degree_seq.sort()
					uniq_sequences.add(tuple(degree_seq))
					degree_seq = []
			else:
				connections = line[line.index(':') + 1:]
				if connections != ' ;\n':
					degree_seq.append(line[line.index(':') + 1:].count(' '))
				else:
					degree_seq.append(0)
	degree_seq.sort()
	uniq_sequences.add(tuple(degree_seq))
	sequences = list(uniq_sequences)
	sequences.sort()
	for sequence in sequences:
		print(sequence)

if __name__ == '__main__':
	get_unique_degree_sequences(sys.argv[1])
