from typing import Callable

from data.games import Games
from utils.cli import console


def _confirm_will_delete(warning_message: str) -> bool:
    console.print(warning_message)
    console.print(f'Enter "delete" to confirm, or anything else to cancel:')
    user_input = console.input('>> ')
    return user_input.strip().lower() == 'delete'


def delete_from_games(games: Games, func: Callable, selected_systems: list, message: str):
    # TODO: Maybe extract into 2 functions:
    # - clear_seen()
    # - delete_gamelists()

    warning_message = (
        f'[bold red]WARNING: [/bold red][red]{message}[/red][orange1]'
        f'{' '.join(selected_systems)}[/orange1]'
    )
    if not _confirm_will_delete(warning_message):
        return
    func(selected_systems)
    games.save()