#! /usr/bin/python
import sys
import itertools

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def compress_sequence(sequence):
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
	return ''.join(s)

def main(args):
	if len(args) < 2:
		eprint('usage: full_bipartite_degree_sequences.py [-c] [-s] vertices')
		eprint('	-c prints graph_count')
		eprint('	-s prints sequences')
		eprint('	-sc prints sequence_count')
		eprint('	-sr prints sequence (with repeats) for each graph')
		eprint('	-pg prints graphs')
		eprint('	-pssg prints graphs with same degree sequences')
		eprint('	-cbg prints number of complete bipartite subgraph for each graph')
		return 1

	flags = {
		'-c'    : 'print_count',
		'-s'    : 'print_sequences',
		'-sc'   : 'print_sequence_count',
		'-sr'   : 'print_sequences_repeat',
		'-pg'   : 'print_graphs',
		'-pssg' : 'print_same_seq_graphs',
		'-cbg'   : 'print_complete_bipartite_graph_count',
	}

	tripped_flags = set()
	n = None
	for arg in args[1:]:
		if arg in flags:
			tripped_flags.add(flags[arg])
			continue
		try:
			n = int(arg)
		except ValueError:
			eprint('unknown argument: ' + arg)
			return 1

	if n is None:
		eprint('missing argument: vertices')
		return 1
	elif n < 2:
		eprint('vertices must be greater than or equal to 2')
		return 1

	if len(tripped_flags) == 0:
		eprint('you must use one flag (-c, -s, -sc, -pg)')
		return 1

	data = full_bipartite_degree_sequences(n,
			'print_graphs' in tripped_flags,
			'print_same_seq_graphs' in tripped_flags,
			'print_sequences_repeat' in tripped_flags,
			'print_complete_bipartite_graph_count' in tripped_flags)

	if 'print_count' in tripped_flags:
		print(f'graphs (vertices: {n}):', data[1])

	if 'print_sequence_count' in tripped_flags:
		print(f'sequences (vertices: {n}):', len(data[0]))

	if 'print_sequences' in tripped_flags:
		for sequence in sorted(data[0], reverse=True):
			print(sequence)

	return 0

def full_bipartite_degree_sequences(n, print_graphs=False, print_same_seq_graphs=False,
		print_sequences_repeat=False, print_complete_bipartite_graph_count=False):
	"""
	n: number of vertices

	sequences is a set of all unique degree sequences for full bipartite graphs
	of order n
	return (sequences, graph_count)
	"""
	sequences = {}
	graph_count = 0
	for combination in sum_combinations(n, 2, n//2):
		for sequence, graph in degree_sequences(compositions(combination)):
			if print_graphs:
				print(graph)
			if print_sequences_repeat:
				print(sequence)
			if print_complete_bipartite_graph_count:
				print(len(graph))
			graph_count += 1
			if sequence in sequences:
				sequences[sequence].append(graph)
			else:
				sequences[sequence] = [graph]

	if print_same_seq_graphs:
		for sequence in sorted(sequences, reverse=True):
			if len(sequences[sequence]) == 1: continue
			print(f'sequence: {compress_sequence(sequence)}')
			print('graphs:')
			for graph in sorted(sequences[sequence], reverse=True):
				print(f'\t{graph}')
			print()

	return (sequences, graph_count)

def compositions(combination):
	""" returns all the compositions of a combination in compressed form """
	return tuple((tuple(complete_bipartites(order)) for order in combination))

def complete_bipartites(order):
	start = order - 1
	end = (order // 2) - 1 if order % 2 == 0 else (order // 2)
	for left in range(start, end, -1):
		right = order - left
		yield (left, right)

def sort_graph(graph):
	result = sorted(map(lambda x: tuple(sorted(x, reverse=True)), graph), reverse=True)
	return tuple(result)

def unpack_compositions(compositions):
	graphs = map(sort_graph, itertools.product(*compositions))
	unique_graphs = set()
	for graph in graphs:
		if graph not in unique_graphs:
			unique_graphs.add(graph)
			yield graph

def degree_sequences(compositions):
	for full_bipartite_graph in unpack_compositions(compositions):
		yield (degree_sequence(full_bipartite_graph), full_bipartite_graph)

def degree_sequence(full_bipartite_graph):
	sequence = []
	for complete_bipartite_graph in full_bipartite_graph:
		left, right = complete_bipartite_graph
		for _ in range(left):
			sequence.append(right)
		for _ in range(right):
			sequence.append(left)
	sequence.sort(reverse=True)
	return tuple(sequence)

def sum_combinations(total, low_bound, max_length):
	"""
	returns a list of all combinations of integers >= low_bound that add up to
	total, the length of the list does not exceed max_length
	"""
	combinations = []
	_sum_combinations(combinations, [], 0, total, low_bound, max_length)
	return combinations

def _sum_combinations(combinations, current, current_sum, total, low_bound, max_length):
	assert len(current) <= max_length

	difference = total - current_sum
	if current_sum == total:
		combinations.append(tuple(current))
		return
	if current_sum > total or difference < low_bound or len(current) >= max_length:
		return

	max_summand = total if len(current) == 0 else min(difference, current[-1])
	for n in range(max_summand, low_bound - 1, -1):
		current.append(n)
		_sum_combinations(combinations, current, current_sum + n, total, low_bound, max_length)
		current.pop(-1)

if __name__ == '__main__':
	exit(main(sys.argv))
