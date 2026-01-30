from floyd.adapters.inbound.cli import ui
from floyd.adapters.outbound.ai.ai_adapter import AIAdapter
from floyd.application.dto.ai_config import AIConfig
from floyd.domain.entities.git_context import GitContext
from floyd.domain.entities.pull_request import PullRequest

class CopilotAdapter(AIAdapter):

    def generate_draft(
        self,
        context: GitContext,
        config: AIConfig,
        feedback: str | None = None,
    ) -> PullRequest:
        prompt = self._build_prompt(context, config, feedback)

        command = ["copilot", "-p", "-"]

        if config.model:
            command.extend(["--model", config.model])
            ui.show_info(f"Copilot is using the model: {config.model}")

        response = self.terminal.run(
            command, 
            input_data=prompt, 
            error_msg="GitHub Copilot CLI"
        )

        return self._parse_response(response, context.current_branch.name)
