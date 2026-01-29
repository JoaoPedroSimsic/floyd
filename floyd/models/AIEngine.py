from floyd.dtos import AIConfigDTO
from floyd.dtos import GitContextDTO
from floyd.dtos import PullRequestDTO


class AIEngine:
    def __init__(self, config: AIConfigDTO) -> None:
        self.config = config

    def generate_draft(self, ctx: GitContextDTO) -> PullRequestDTO:
        processed_diff = self._limit_diff(ctx.diff)

        prompt = self._build_propmt(ctx, processed_diff)

        raw_response = run_command(["claude", "-p", prompt])

        return self._parse_response(raw_response)
