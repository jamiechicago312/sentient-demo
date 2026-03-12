from __future__ import annotations

import os
from pathlib import Path

from openhands.sdk import Agent, Conversation, LLM, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool


def run_openhands_doc_agent(*, workspace: Path, prompt: str, llm_model: str, llm_api_key: str, llm_base_url: str | None) -> None:
    llm = LLM(
        model=llm_model,
        api_key=llm_api_key,
        base_url=llm_base_url,
    )

    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
    )

    conversation = Conversation(agent=agent, workspace=str(workspace))

    # Make shell commands deterministic (TerminalTool inherits current working directory).
    os.chdir(workspace)

    conversation.send_message(prompt)
    conversation.run()
