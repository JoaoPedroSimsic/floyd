"""Terminal UI utilities for CLI adapter."""

from contextlib import contextmanager
from typing import Generator

import questionary
from rich.color import Color
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status
from rich.text import Text

from floyd.domain.entities.pull_request import PullRequest

console = Console()

START_COLOR = "#F54800"
END_COLOR = "#F5B800"

MAIN_COLOR = "#F59A00"
SEC_COLOR = "#F5D500"

ICON = """


 ███████████ █████          ███████    █████ █████ ██████████
░░███░░░░░░█░░███         ███░░░░░███ ░░███ ░░███ ░░███░░░░███
 ░███   █ ░  ░███        ███     ░░███ ░░███ ███   ░███   ░░███
 ░███████    ░███       ░███      ░███  ░░█████    ░███    ░███
 ░███░░░█    ░███       ░███      ░███   ░░███     ░███    ░███
 ░███  ░     ░███      █░░███     ███     ░███     ░███    ███
 █████       ███████████ ░░░███████░      █████    ██████████
░░░░░       ░░░░░░░░░░░    ░░░░░░░       ░░░░░    ░░░░░░░░░░




"""


def _get_transition_color(start_hex: str, end_hex: str, fraction: float) -> str:
    """Calculate transition color between two hex colors.

    Args:
        start_hex: Starting color in hex format.
        end_hex: Ending color in hex format.
        fraction: Fraction between 0 and 1 for interpolation.

    Returns:
        RGB color string.
    """
    start_rgb = Color.parse(start_hex).get_truecolor()
    end_rgb = Color.parse(end_hex).get_truecolor()

    r = int(start_rgb.red + (end_rgb.red - start_rgb.red) * fraction)
    g = int(start_rgb.green + (end_rgb.green - start_rgb.green) * fraction)
    b = int(start_rgb.blue + (end_rgb.blue - start_rgb.blue) * fraction)

    return f"rgb({r},{g},{b})"


def show_icon() -> None:
    """Display the Floyd ASCII art logo with gradient colors."""
    stretch = 1.0

    lines = ICON.splitlines()
    if not lines:
        return

    max_y = len(lines)
    max_x = max(len(line) for line in lines)
    max_distance = max_x + max_y

    for y, line in enumerate(lines):
        rich_line = Text()
        for x, char in enumerate(line):
            distance = x + y

            fraction = distance / (max_distance * stretch)
            fraction = max(0.0, min(1.0, fraction))

            color = _get_transition_color(START_COLOR, END_COLOR, fraction)
            rich_line.append(char, style=color)

        console.print(rich_line)


def show_error(message: str) -> None:
    """Display an error message.

    Args:
        message: Error message to display.
    """
    console.print(f"[bold red]{message}[/bold red]")


def show_info(message: str) -> None:
    """Display an info message.

    Args:
        message: Info message to display.
    """
    console.print(f"[gray]{message}[/gray]")


@contextmanager
def show_loading(message: str = "Working...") -> Generator[Status, None, None]:
    """Display a loading spinner.

    Args:
        message: Loading message to display.

    Yields:
        Rich Status object.
    """
    with console.status(
        f"[gray]{message}[/gray]",
        spinner="dots",
        spinner_style=SEC_COLOR,
    ) as status:
        yield status


def show_warning(message: str) -> None:
    """Display a warning message.

    Args:
        message: Warning message to display.
    """
    console.print(f"[bold yellow]{message}[/bold yellow]")


def show_success(message: str) -> None:
    """Display a success message.

    Args:
        message: Success message to display.
    """
    console.print(f"[bold green]{message}[/bold green]")


def _get_gradient_text(text: str, bold: bool = True) -> Text:
    """Creates a Rich Text object with a color gradient."""
    if not text:
        return Text("")

    rich_text = Text()
    length = len(text)
    denom = (length - 1) if length > 1 else 1

    for i, char in enumerate(text):
        fraction = i / denom
        color = _get_transition_color(START_COLOR, END_COLOR, fraction)
        style = f"bold {color}" if bold else color
        rich_text.append(char, style=style)

    return rich_text


def display_draft(pr: PullRequest) -> None:
    """Display a PR draft in a formatted panel.

    Args:
        pr: PullRequest entity to display.
    """
    padding = (1, 3)

    console.print(
        Panel(
            Text(pr.title, style="white"),
            title=_get_gradient_text(" Title "),
            title_align="left",
            border_style=MAIN_COLOR,
            padding=padding,
        )
    )

    console.print(
        Panel(
            pr.body,
            title=_get_gradient_text(" Body "),
            title_align="left",
            border_style=MAIN_COLOR,
            padding=padding,
        )
    )


def get_refinement_feedback() -> str:
    """Prompt user for refinement feedback.

    Returns:
        User's feedback string.
    """
    return Prompt.ask("[bold yellow]What should I change?[/bold yellow]")


def get_action_choice() -> str | None:
    """Prompt user to choose an action.

    Returns:
        User's choice: 'create', 'refine', or 'cancel'. None if interrupted.
    """
    custom_style = questionary.Style(
        [
            ("qmark", f"fg:{SEC_COLOR} bold"),
            ("question", "bold"),
            ("pointer", f"fg:{MAIN_COLOR} bold"),
            ("highlighted", f"fg:{MAIN_COLOR} bold"),
            ("selected", f"fg:{MAIN_COLOR}"),
            ("answer", f"fg:{SEC_COLOR} bold"),
        ]
    )

    result: str | None = questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice(title="Create Pull Request", value="create"),
            questionary.Choice(title="Refine Draft", value="refine"),
            questionary.Choice(title="Cancel", value="cancel"),
        ],
        style=custom_style,
        pointer="❯",
    ).ask()

    return result
