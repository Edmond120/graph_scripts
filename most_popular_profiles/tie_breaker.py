import sys
from ast import literal_eval

def break_tie(filename):
	top_seq = (0, ())
	with open(filename, 'r') as file:
		for line in file:
			line = line.strip()
			sep_pos = line.index(' ')
			count = int(line[:sep_pos])
			sequence = literal_eval(line[sep_pos+1:])
			if count < top_seq[0]:
				print_top_seq(top_seq)
				exit()
			if sequence > top_seq[1]:
				top_seq = (count, sequence)
	print_top_seq(top_seq)

def print_top_seq(top_seq):
	print(f'{top_seq[0]},{compress_seq(top_seq[1])}')

def compress_seq(sequence):
	counts = {}
	for degree in sequence:
		if degree in counts:
			counts[degree] += 1
		else:
			counts[degree] = 1
	s = ['(']
	for num in sorted(counts, reverse=True):
		s.append(str(num))
		s.append('^')
		s.append(str(counts[num]))
		s.append(',')
	s.pop(-1)
	s.append(')')
	return ''.join(s)

if __name__ == '__main__':
	break_tie(sys.argv[1])
