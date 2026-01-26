from typing import Callable

from data.games import Games
from common.console import console


def confirm_delete(func: Callable):
    def wrapper(*args, **kwargs):
        console.print(f'Enter "delete" to confirm, or anything else to cancel:')
        user_input = console.input('>> ')
        if user_input.strip().lower() == 'delete':
            console.print('[yellow]Deleted.[/yellow]')
            return func(*args, **kwargs)
        console.print('[yellow]Cancelled.[/yellow]')
    return wrapper


def print_system_list_warning(describe_action: str, selected_systems: list):
    console.print(
        f'[bold red]WARNING: [/bold red][red]You are about to {describe_action.strip()} '
        f'for the following system/s: [/red][orange1]{' '.join(selected_systems)}[/orange1]'
    )


@confirm_delete
def clear_seen_games(games: Games, selected_systems: list):
    Games.clear_seen(games.data, selected_systems)
    games.save()


@confirm_delete
def delete_games(games: Games, selected_systems: list):
    games.clear(selected_systems)
    games.save()