from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.color import Color
from contextlib import contextmanager
import questionary

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


def get_transition_color(start_hex, end_hex, fraction):
    start_rgb = Color.parse(start_hex).get_truecolor()
    end_rgb = Color.parse(end_hex).get_truecolor()

    r = int(start_rgb.red + (end_rgb.red - start_rgb.red) * fraction)
    g = int(start_rgb.green + (end_rgb.green - start_rgb.green) * fraction)
    b = int(start_rgb.blue + (end_rgb.blue - start_rgb.blue) * fraction)

    return f"rgb({r},{g},{b})"


def show_icon():
    STRETCH = 1.0

    lines = ICON.strip("\n").splitlines()
    if not lines:
        return

    max_y = len(lines)
    max_x = max(len(line) for line in lines)
    max_distance = max_x + max_y

    for y, line in enumerate(lines):
        rich_line = Text()
        for x, char in enumerate(line):
            distance = x + y

            fraction = distance / (max_distance * STRETCH)

            fraction = max(0.0, min(1.0, fraction))

            color = get_transition_color(START_COLOR, END_COLOR, fraction)
            rich_line.append(char, style=color)

        console.print(rich_line)


def show_error(message):
    console.print(f"[bold red]{message}[/bold red]")


def show_info(message):
    console.print(f"[gray]{message}[/gray]")


@contextmanager
def show_loading(message="Working..."):
    with console.status(
        f"[gray]{message}[/gray]",
        spinner="dots",
        spinner_style=SEC_COLOR,
    ) as status:
        yield status


def show_warning(message):
    console.print(f"[bold yellow]{message}[/bold yellow]")


def show_success(message):
    console.print(f"[bold green]{message}[/bold green]")


def display_draft(title, body):
    padding = (1, 3)

    console.print(
        Panel(
            f"[bold {SEC_COLOR}]Title:[/bold {SEC_COLOR}] {title}\n\n[bold {SEC_COLOR}]Body:[/bold {SEC_COLOR}]\n{body}",
            title=f"[{SEC_COLOR}]Draft Pull Request[/{SEC_COLOR}]",
            border_style=MAIN_COLOR,
            padding=padding,
        )
    )


def get_refinement_feedback():
    return Prompt.ask("[bold yellow]What should I change?[/bold yellow]")


def get_action_choice():
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

    return questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice(title="Create Pull Request", value="create"),
            questionary.Choice(title="Refine Draft", value="refine"),
            questionary.Choice(title="Cancel", value="cancel"),
        ],
        style=custom_style,
        pointer="❯",
    ).ask()
