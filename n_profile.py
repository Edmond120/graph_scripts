#! /usr/bin/python
import sys
from lib.neighborhood_profile_tools import *
from inspect import getdoc
from ast import literal_eval

flags = {
	'-h' : 'help',
	'--help' : 'help',
}
tripped_flags = set()
commands = {}

def command(name=None):
	"""decorator, adds function in dict commands with <name> as key.
	if <name> is None then the name of the function is used instead"""
	def decorator(function):
		key = name if name is not None else function.__name__
		commands[key] = function
		return function
	return decorator

def help_message():
	header = """Usage: python tools.py [FLAGS] [COMMAND [ARGS...]]
	Flags:
		-h | --help : print this message

	Commands:"""
	message = [header]
	for command in sorted(commands):
		lines = getdoc(commands[command])
		lines = [] if lines is None else lines.split('\n')
		for i in range(len(lines)):
			lines[i] = '\t' * 3 + lines[i]
		message.append(f'\t\t{command}:')
		message.append('\n'.join(lines))

	return '\n'.join(message).replace('\t',' ' * 4)

def eprint(*args, **kwargs):
	print(*args, **kwargs, file=sys.stderr)

def main(args):
	if len(args) <= 1:
		print(help_message())
		return 0
	for i in range(1, len(args)):
		arg = args[i]
		if arg in flags:
			tripped_flags.add(flags[arg])
			if flags[arg] == 'help':
				print(help_message())
				return 0
		elif arg in commands:
			error_code = commands[arg](args[i+1:])
			if error_code is None:
				return 0
			return error_code
		else:
			eprint('unknown argument:', arg)
			return 1
	return 0

@command('profile')
def n_profile(args, *, simple=False):
	"args: <Imax,Imin,Emax,Emin> <filename>"
	profile_type, filename = args
	profile_func = {
		'Imax' : get_Imax_profile,
		'Imin' : get_Imin_profile,
		'Emax' : get_Emax_profile,
		'Emin' : get_Emin_profile,
	}[profile_type]
	if simple:
		for profile in profiles_in_file(filename, profile_func):
			print(profile)
	else:
		for profile in sorted(set(profiles_in_file(filename, profile_func)), reverse=True):
			print(profile)

@command('profile_simple')
def n_profile_simple(args):
	"""same as profile except the order of the profiles matches the
	order of the graphs. Will not filter for unique profiles nor sort them."""
	n_profile(args, simple=True)

@command('profile_count')
def n_profile_count(args):
	"args: <Imax,Imin,Emax,Emin> <filename> [<filename> ...]"
	profile_type = args[0]
	filenames = args[1:]
	profile_func = {
		'Imax' : get_Imax_profile,
		'Imin' : get_Imin_profile,
		'Emax' : get_Emax_profile,
		'Emin' : get_Emin_profile,
	}[profile_type]
	for filename in filenames:
		print(f'{filename}: {len(set(profiles_in_file(filename, profile_func)))}')

@command('fb_n_profile')
def full_bipartite_graph_n_profiles(args, *, simple=False):
	"""args: <Imax,Emax,Imin,Emin> <filename>
	file is in the format of full_bipartie_degree_sequences.py -pg <n>"""
	profile_name, filename = args
	profile_func = {
		'Imax' : lambda s: max(s),
		'Emax' : lambda s: max(s[:-1]),
		'Imin' : lambda s: min(s),
		'Emin' : lambda s: min(s[:-1]),
	}[profile_name]
	with open(filename, 'r') as file:
		profiles = []
		for line in file:
			fb = literal_eval(line)
			profile = []
			for cb in fb:
				left, right = cb
				for _ in range(left):
					profile.append(profile_func( (left,) * right + (right,) ))
				for _ in range(right):
					profile.append(profile_func( (right,) * left + (left,) ))
			profile.sort(reverse=True)
			profiles.append(tuple(profile))
		if simple:
			for line in profiles:
				print(line)
		else:
			for p in sorted(set(profiles), reverse=True):
				print(p)

@command('fb_n_profile_simple')
def simple_fbg_n_profiles(args):
	"""same as fb_n_profile except the order of the profiles matches the
	order of the graphs. Will not filter for unique profiles nor sort them."""
	full_bipartite_graph_n_profiles(args, simple=True)

if __name__ == '__main__':
	exit(main(sys.argv))
