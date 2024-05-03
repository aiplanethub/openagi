import uuid
from abc import ABC, abstractmethod
from queue import Queue
from typing import Dict, List, Tuple


# Action as an abstract base class
class Action(ABC):
    @abstractmethod
    def execute(self, context: Dict) -> None:
        pass


# Concrete actions implementing the Action interface
class WebSearch(Action):
    def execute(self, context: Dict) -> None:
        print("Performing Web Search...")
        # Example of adding data to the context
        context["web_search_result"] = "Web search data"


class WikiSearch(Action):
    def execute(self, context: Dict) -> None:
        print("Performing Wiki Search...")
        context["wiki_search_result"] = "Wiki search data"


class Summarizer(Action):
    def execute(self, context: Dict) -> None:
        print("Summarizing information...")
        web_data = context.get("web_search_result", "")
        wiki_data = context.get("wiki_search_result", "")
        context["summary"] = f"Summary of {web_data} and {wiki_data}"


class Compressor(Action):
    def execute(self, context: Dict) -> None:
        print("Compressing data...")
        summary = context.get("summary", "")
        context["compressed_summary"] = f"Compressed: {summary}"


# Worker class that can hold multiple actions and belongs to a team
class Worker:
    def __init__(
        self, name: str, actions: List[Action], team_name: str = None, llm=None
    ):
        self.name = name
        self.actions = actions
        self.team_name = team_name
        self.llm = llm

    def perform_actions(self, context: Dict) -> None:
        if not self.llm:
            raise ValueError(f"LLM is not set for worker {self.name}.")
        print(
            f"Worker ({self.name}) with LLM {self.llm} executing actions for team '{self.team_name}'..."
        )
        for action in self.actions:
            action.execute(context)


class BasePromptTemplate:
    def __init__(self) -> None:
        pass


# Planner to manage execution flow
class Planner:
    def __init__(self, actions: List[Action], human_intervene: bool = True, llm=None):
        self.actions = actions
        self.human_intervene = human_intervene
        self.llm = llm

    def plan(self, objective: str):
        print


class STMemory:
    def __init__(self) -> None: ...

    def add(self): ...

    def get(self): ...


class LTMemory:
    def __init__(self) -> None: ...

    def add(self): ...

    def get(self): ...

    def dump_from_st(self, st): ...


# Admin to manage the planner, single workers, and teams of workers
class Admin:
    def __init__(self, planner: Planner, llm: str = None):
        self.planner: Planner = planner
        self.llm = llm
        self.teams = []
        self.single_workers = []
        self.st_memory: STMemory = STMemory()
        self.lt_memory: LTMemory = LTMemory()

    def add_team(self, team: List[Worker]) -> None:
        self.teams.append(team)

    def create_and_add_team(
        self, team_name: str, team_members: List[Tuple[str, List[Action], str]]
    ) -> None:
        team = []
        for name, actions, llm in team_members:
            if not llm:
                if not self.llm:
                    raise ValueError(
                        f"No LLM set for worker {name} and no default LLM available in Admin."
                    )
                llm = self.llm
            worker = Worker(name, actions, team_name, llm)
            team.append(worker)
        self.add_team(team)

    def add_single_worker(self, worker: Worker) -> None:
        if not worker.llm:
            if not self.llm:
                raise ValueError(
                    "No LLM set for the worker and no default LLM available in Admin."
                )
            worker.llm = self.llm
        self.single_workers.append(worker)

    def run(self, objective: str) -> None:
        if not getattr(self.planner, "llm"):
            self.planner.llm = self.planner.llm or self.llm

        self.planner.plan(objective)
        context = {}  # Shared context
        print("Running tasks...")
        print(f"Task Objective: {objective}")

        # Run individual workers
        for worker in self.single_workers:
            worker.perform_actions(context)

        # Run teams of workers
        for team in self.teams:
            for worker in team:
                worker.perform_actions(context)

        # Store the context in memory with a unique identifier
        self.st_memory.add(context)

        self.lt_memory.dump_from_st(self.st_memory)
        # Output final context for demonstration
        print("Final Context:", context)

    def recall_memory(self, task_id):
        """Retrieve stored data from memory by task ID."""
        return self.st_memory.get(task_id, "No record found for this task ID.")


class Task:
    def __init__(self, query) -> None:
        self.id = uuid.uuid4()
        self.query = query
        self.result = None  # Store the result of the task


class Tasks:
    def __init__(self) -> None:
        self.tasks = Queue()

    def add_task(self, task: Task) -> None:
        """Adds a Task instance to the queue."""
        self.tasks.put(task)

    def get_next_unprocessed_task(self) -> Task:
        """Retrieves the next unprocessed task from the queue."""
        if not self.tasks.empty():
            return self.tasks.get_nowait()
        return None

    def all_tasks_processed(self):
        """Checks if all tasks in the queue have been processed."""
        return self.tasks.empty()


# Example usage
if __name__ == "__main__":
    # Create a planner
    actions = [WebSearch(), Summarizer()]
    p = Planner(actions=actions, human_intervene=True)

    # Create an admin with a default LLM
    admin_agent = Admin(planner=p, llm="OpenAI")

    # Add single workers
    worker1 = Worker(
        "SoloSearch", [WebSearch()], llm=None
    )  # LLM will be set from Admin
    admin_agent.add_single_worker(worker1)

    # Create and add teams to admin
    team1_members = [
        ("Searcher", [WebSearch()], None),
        ("Processor", [Summarizer()], None),
    ]
    admin_agent.create_and_add_team("Team 1", team1_members)

    # Run the system
    admin_agent.run("Get financial records of Coca-Cola for the past 5 years")
