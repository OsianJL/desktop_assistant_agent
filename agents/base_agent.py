from langchain.agents import initialize_agent, Tool, AgentExecutor  # type: ignore
from langchain.agents.agent_types import AgentType
from langchain.tools import BaseTool
from config.settings import get_openai_model
from tools.hello_tool import say_hello
from tools.tool_loader import load_all_tools
from typing import List


def create_agent() -> AgentExecutor:
    manual_tools: List[BaseTool] = [
        Tool(
            name="Saludo",
            func=say_hello,
            description="Devuelve un saludo simple. Úsalo cuando te pidan saludar.",
        ),
    ]

    dynamic_tools = load_all_tools()  # ← lo que cargue el ToolLoader

    tools = manual_tools + dynamic_tools

    llm = get_openai_model()
    return initialize_agent(
        tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
