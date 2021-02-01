#! /usr/bin/python
import sys

def main(args):
	if len(args) < 2:
		print('args: <file_name>')
		return
	with open(args[1], 'r') as file:
		for line in file:
			sequence = tuple(map(int, line.strip('()\n ').split(',')))
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
				s.append(', ')
			s.pop(-1)
			s.append(')')
			print(''.join(s))

if __name__ == '__main__':
	main(sys.argv)
