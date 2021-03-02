import subprocess
import sys

def parse_graph_file(file_):
	"""takes a file name and returns a generator of graphs
	graphs implemented as a dictionary """
	with subprocess.Popen(['showg', '-q', file_], stdout=subprocess.PIPE).stdout as pipe:
		graph_lines = []
		for line in pipe:
			line = line.decode('utf-8')
			if line.count(':') == 0:
				if len(graph_lines) != 0:
					yield make_graph(tuple(graph_lines))
					graph_lines.clear()
			else:
				graph_lines.append(line[:-2])
		yield make_graph(tuple(graph_lines))

def make_graph(lines):
	graph = {}
	for line in lines:
		head, tail = map(lambda s: s.strip(' ;'), line.split(':'))
		vertex = int(head)
		edges = tuple(map(int, tail.split()))
		graph[vertex] = edges
	return graph
