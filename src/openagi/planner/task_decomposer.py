from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.actions.human_input import HumanCLIInput
from openagi.exception import LLMResponseError
from openagi.llms.azure import LLMBaseModel
from openagi.planner.base import BasePlanner
from openagi.prompts.base import BasePrompt
from openagi.prompts.task_creator import SingleAgentTaskCreator, MultiAgentTaskCreator
from openagi.utils.extraction import extract_ques_and_task, get_last_json
from openagi.worker import Worker


class TaskPlanner(BasePlanner):
    human_intervene: bool = Field(
        default=True, description="If human internvention is required or not."
    )
    input_action: Optional[BaseAction] = Field(
        default=HumanCLIInput,
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: Optional[BasePrompt] = Field(description="Prompt to be used")
    llm: Optional[LLMBaseModel] = Field(default=None, description="LLM Model to be used")

    def get_prompt(self) -> None:
        prompt = self.prompt
        if not self.prompt:
            if self.workers:
                self.prompt = SingleAgentTaskCreator()
            else:
                self.prompt = MultiAgentTaskCreator(workers=self.workers)
        return prompt

    def _extract_task_from_response(self, llm_response: str) -> Union[str, None]:
        return get_last_json(llm_response)

    def _should_clarify(self, query: Optional[str]) -> bool:
        if query and len(query) > 0:
            return True
        return False

    def plan(
        self, query: str, description: str, supported_actions: List[Dict], *args, **kwargs
    ) -> Dict:
        planner_vars = dict(
            objective=query,
            task_descriptions=description,
            supported_actions=supported_actions,
            *args,
            **kwargs,
        )
        prompt: str = self.prompt.from_template(
            variables=planner_vars,
        )
        resp = self.llm.run(prompt)

        prompt, ques_to_human = extract_ques_and_task(resp)

        while self.human_intervene and self._should_clarify(ques_to_human):
            human_intervene = self.input_action(ques_prompt=ques_to_human)
            human_resp = human_intervene.execute()
            prompt = f"{prompt}\n{ques_to_human}\n{human_resp}"
            resp = self.llm.run(prompt)
            prompt, ques_to_human = extract_ques_and_task(resp)

        tasks = self._extract_task_from_response(llm_response=resp)
        if not tasks:
            raise LLMResponseError("No tasks found in the Planner response.")

        return tasks
