import subprocess
from rich.console import Console
import shlex

from floyd.domain.exceptions.pr.pr_generation_exception import PRGenerationException


class Terminal:
    def __init__(self):
        self.console = Console()

    def run(self, command: list[str] | str, error_msg: str = "Command Failed") -> str:
        cmd_list = shlex.split(command) if isinstance(command, str) else command

        try:
            result = subprocess.run(
                cmd_list, capture_output=True, text=True, check=True
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            detail = e.stderr.strip() or str(e)

            raise PRGenerationException(f"{error_msg}: {detail}") from None
        except FileNotFoundError:
            raise PRGenerationException(
                f"The tool '{cmd_list[0]}' was not found. Please ensure it is installed."
            )
