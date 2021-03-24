#! /usr/bin/python
import sys
from ast import literal_eval
from inspect import getdoc

commands = {}
def command(name=None):
	def decorator(func):
		func_name = func.__name__ if name is None else name
		commands[func_name] = func
		return func
	return decorator

def print_help_message():
	print('Usage: converter.py <command> [<command arg>...]')
	for command_name in commands:
		command = commands[command_name]
		doc = getdoc(command)
		if len(doc) == 0:
			print(command.__name__)
			print()
			continue
		print(command.__name__ + ':')
		for line in doc.split('\n'):
			print('\t', end='')
			print(line)
		print()

def main(argv):
	argv = argv[1:]
	if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
		print_help_message()
		return 0
	if argv[0] in commands:
		error_num = commands[argv[0]](argv[1:])
		return 0 if error_num is None else error_num
	print('invalid command')
	return 0

@command()
def fbg_to_showg(args):
	"""Reads data from stdin and outputs in showg format.
	Input data is in the format of full_bipartite_degree_sequences.py -pg n
	"""
	graph_count = 1
	for line in sys.stdin:
		print()
		fg_graph_data = literal_eval(line)
		node_label = 0
		graph = []
		for complete_biparite_graph in fg_graph_data:
			left_count, right_count = reversed(complete_biparite_graph)
			left_nodes = []
			right_nodes = []
			for _ in range(left_count):
				left_nodes.append(node_label)
				node_label += 1
			for _ in range(right_count):
				right_nodes.append(node_label)
				node_label += 1
			# Only need to store the numbers pass ':' in showg.
			# The indicies are the graph labels on the left of the ':'.
			for _ in left_nodes:
				graph.append(right_nodes.copy())
			for _ in right_nodes:
				graph.append(left_nodes.copy())

		print(f'Graph {graph_count}, order {len(graph)}.')
		graph_count += 1
		for i in range(len(graph)):
			print(f'  {i} :', end='')
			for node in graph[i]:
				print(f' {node}', end='')
			print(';')

if __name__ == '__main__':
	exit(main(sys.argv))
