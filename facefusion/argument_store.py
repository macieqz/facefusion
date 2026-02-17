from argparse import Action
from typing import List

from facefusion.types import Argument, ArgumentSet, ArgumentStore, Arguments, Scope

ARGUMENT_STORE : ArgumentStore =\
{
	'api': {},
	'cli': {},
	'sys': {}
}


def get_api_set() -> ArgumentSet:
	return ARGUMENT_STORE.get('api')


def get_cli_set() -> ArgumentSet:
	return ARGUMENT_STORE.get('cli')


def get_sys_set() -> ArgumentSet:
	return ARGUMENT_STORE.get('sys')


def get_api_arguments() -> List[str]:
	return list(get_api_set().keys())


def get_cli_arguments() -> List[str]:
	return list(get_cli_set().keys())


def get_sys_arguments() -> List[str]:
	return list(get_sys_set().keys())


def register_arguments(actions : List[Action], scopes : List[Scope]) -> None:
	for action in actions:
		value : Argument =\
		{
			'default': action.default
		}

		if action.choices:
			value['choices'] = list(action.choices)

		for scope in scopes:
			if scope == 'api':
				ARGUMENT_STORE['api'][action.dest] = value
			if scope == 'cli':
				ARGUMENT_STORE['cli'][action.dest] = value
			if scope == 'sys':
				ARGUMENT_STORE['sys'][action.dest] = value


def filter_api_arguments(arguments : Arguments) -> Arguments:
	api_arguments =\
	{
		key: arguments.get(key) for key in arguments if key in get_api_set() #type:ignore[literal-required]
	}
	return api_arguments


def filter_cli_arguments(arguments : Arguments) -> Arguments:
	cli_arguments =\
	{
		key: arguments.get(key) for key in arguments if key in get_cli_arguments() #type:ignore[literal-required]
	}
	return cli_arguments


def filter_step_arguments(arguments : Arguments) -> Arguments:
	step_arguments =\
	{
		key: arguments.get(key) for key in arguments if key in get_cli_arguments() and key not in get_sys_set() #type:ignore[literal-required]
	}
	return step_arguments


def filter_sys_arguments(arguments : Arguments) -> Arguments:
	sys_arguments =\
	{
		key: arguments.get(key) for key in arguments if key in get_sys_set() #type:ignore[literal-required]
	}
	return sys_arguments
