from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

ICON = """
 🤖 [bold cyan]AI-PR GENERATOR[/bold cyan]
 [dim]Transforming diffs into descriptions[/dim]
"""


def show_icon():
    console.print(ICON)


def show_error(message):
    console.print(f"[bold red]❌ {message}[/bold red]")


def show_info(message):
    console.print(f"[bold blue]🔍 {message}[/bold blue]")


def show_warning(message):
    console.print(f"[bold yellow]⚠️ {message}[/bold yellow]")


def show_success(message):
    console.print(f"[bold green]🚀 {message}[/bold green]")


def display_draft(title, body):
    console.print(
        Panel(
            f"[bold]TITLE:[/bold] {title}\n\n[bold]BODY:[/bold]\n{body}",
            title="[magenta]Draft Pull Request[/magenta]",
            border_style="cyan",
        )
    )


def get_action_choice():
    return Prompt.ask(
        "What would you like to do?",
        choices=["create", "refine", "cancel"],
        default="create",
    )


def get_refinement_feedback():
    return Prompt.ask("[bold yellow]What should I change?[/bold yellow]")
