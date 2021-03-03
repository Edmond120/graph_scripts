#! /usr/bin/python
import sys
from lib.neighborhood_profile_tools import *
from inspect import getdoc

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

@command('Imax')
def Imax_profiles(args):
	"args: <filename>"
	filename = args[0]
	for profile in sorted(set(profiles_in_file(filename, get_Imax_profile)), reverse=True):
		print(profile)

@command('Imin')
def Imin_profiles(args):
	"args: <filename>"
	filename = args[0]
	for profile in sorted(set(profiles_in_file(filename, get_Imin_profile)), reverse=True):
		print(profile)

@command('Emax')
def Emax_profiles(args):
	"args: <filename>"
	filename = args[0]
	for profile in sorted(set(profiles_in_file(filename, get_Emax_profile)), reverse=True):
		print(profile)

@command('Emin')
def Emin_profiles(args):
	"args: <filename>"
	filename = args[0]
	for profile in sorted(set(profiles_in_file(filename, get_Emin_profile)), reverse=True):
		print(profile)

@command()
def Imax_count(args):
	"args: <filename>"
	filename = args[0]
	print(f'{filename}: {len(set(profiles_in_file(filename, get_Imax_profile)))}')

@command()
def Imin_count(args):
	"args: <filename>"
	filename = args[0]
	print(f'{filename}: {len(set(profiles_in_file(filename, get_Imin_profile)))}')

@command()
def Emax_count(args):
	"args: <filename>"
	filename = args[0]
	print(f'{filename}: {len(set(profiles_in_file(filename, get_Emax_profile)))}')

@command()
def Emin_count(args):
	"args: <filename>"
	filename = args[0]
	print(f'{filename}: {len(set(profiles_in_file(filename, get_Emin_profile)))}')

if __name__ == '__main__':
	exit(main(sys.argv))
