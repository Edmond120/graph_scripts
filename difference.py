#! /usr/bin/python
import sys

def main(args):
	if len(args) < 2:
		print('usage: difference.py <file1> <file2>')
		return 1
	file1 = open(args[0], 'r')
	file2 = open(args[1], 'r')

	while True:
		line1 = file1.readline()
		line2 = file2.readline()
		if line1 == '' and line2 == '':
			break

		num1 = int(line1.split(' ')[-1])
		num2 = int(line2.split(' ')[-1])
		diff = num1 - num2
		print(diff)

	file1.close()
	file2.close()

if __name__ == '__main__':
	exit(main(sys.argv[1:]))
