from typing import Iterator

from agno.agent import Agent
from agno.exceptions import RetryAgentRun
from agno.models.google import Gemini
from agno.tools import FunctionCall, tool

num_calls = 0


def pre_hook(fc: FunctionCall):
    global num_calls

    print(f"Pre-hook: {fc.function.name}")
    print(f"Arguments: {fc.arguments}")
    num_calls += 1
    if num_calls < 2:
        raise RetryAgentRun(
            "This wasn't interesting enough, please retry with a different argument"
        )


@tool(pre_hook=pre_hook)
def print_something(something: str) -> Iterator[str]:
    print(something)
    yield f"I have printed {something}"


agent = Agent(model=Gemini(id="gemini-2.0-flash"), tools=[print_something], markdown=True)
agent.print_response("Print something interesting", stream=True)
