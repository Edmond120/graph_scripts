from .graph_parser import *

def get_n_profile(graph, func, inclusive=True):
	"""The arg 'graph' is a dict with vertices as keys. The values are
	tuples of vertices that are connected to the key.

	The arg 'func' is a function that takes in a tuple of degrees from
	vertices in the neighborhood of 'vertex x', and returns the neighborhood
	profile value of 'vertex x'.

	The arg 'inclusive' determines if the neighborhood profile is an inclusive
	or exclusive neighborhood profile.

	The return value is the neighborhood profile in the form of a list"""
	graph_degrees = {}
	for vertex in graph:
		degree = len(graph[vertex])
		graph_degrees[vertex] = degree

	neighborhood_degree_sequences = []
	for vertex in graph:
		degree_sequence = [ graph_degrees[v] for v in graph[vertex] ]
		if inclusive:
			degree_sequence.append(graph_degrees[vertex])
		neighborhood_degree_sequences.append(degree_sequence)

	n_profile = [func(seq) for seq in neighborhood_degree_sequences]
	n_profile.sort(reverse=True)
	return tuple(n_profile)

def get_Imax_profile(graph):
	return get_n_profile(graph, lambda s: max(s, default=0))

def get_Emax_profile(graph):
	return get_n_profile(graph, lambda s: max(s, default=0), inclusive=False)

def get_Imin_profile(graph):
	return get_n_profile(graph, lambda s: min(s, default=0))

def get_Emin_profile(graph):
	return get_n_profile(graph, lambda s: min(s, default=0), inclusive=False)

def get_Isum_profile(graph):
	return get_n_profile(graph, lambda s: sum(s), inclusive=True)

def get_Esum_profile(graph):
	return get_n_profile(graph, lambda s: sum(s), inclusive=False)

def profiles_in_file(filename, profile_func):
	for graph in parse_graph_file(filename):
		yield profile_func(graph)
