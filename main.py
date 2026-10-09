import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from models import StudyResponse
from tools import (
    calculator,
    get_weather,
    web_search,
)


# Load variables from .env
load_dotenv()


# Read configuration
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")


if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY is missing from .env")

if not LLM_MODEL:
    raise ValueError("LLM_MODEL is missing from .env")


# --------------------------------------------------
# Create OpenRouter model
# --------------------------------------------------

model = OpenRouterModel(
    LLM_MODEL,
    provider=OpenRouterProvider(
        api_key=LLM_API_KEY,
    ),
)


# --------------------------------------------------
# Create PydanticAI agent
# --------------------------------------------------

agent = Agent(
    model,
    output_type=StudyResponse,
    instructions="""
    You are an AI Study Assistant.

    Help the user with:
    - Python
    - programming
    - mathematics
    - Agentic AI
    - weather
    - current information
    - general knowledge

    You have three tools:

    1. Calculator
       Use this for mathematical calculations.

    2. Weather
       Use this for current weather questions.

    3. Web Search
       Use this when the answer requires current, recent,
       latest, changing, real-time, news, or web-based
       information.

    IMPORTANT:

    You decide whether a tool is necessary.

    Do NOT use keywords or fixed rules to decide whether
    web search is required.

    Use your understanding of the user's question.

    If the question can be answered from your existing
    knowledge and does not require a tool, answer directly.

    If mathematics is required, use the calculator tool.

    If current weather information is requested, use the
    weather tool.

    If current or changing information is required, use
    the web_search tool.

    After using a tool, use its result to produce the
    final answer.

    MULTIPLE TASKS AND TOOL ERRORS:

    When a user asks multiple questions or requests multiple
    tasks, try to answer every part.

    If one tool fails, do not abandon the entire request.
    Use results from successful tools to answer the remaining
    parts.

    A weather result with success=false means the weather
    lookup failed. Explain the error returned by the tool.

    Never invent weather data when the weather tool fails.

    A failed weather lookup must not prevent you from
    reporting a successful calculation or other successful
    tool result.

    Do not claim a tool succeeded unless its result supports
    that claim.

    STRUCTURED OUTPUT RULES:

    - used_calculator = true only if the calculator tool
      was actually called.

    - used_weather = true only if the weather tool
      was actually called.

    - used_web_search = true only if the web search tool
      was actually called.

    - If a tool was not used, its value must be false.

    Always return:

    - answer
    - topic
    - difficulty
    - used_calculator
    - used_weather
    - used_web_search
    """,
)


# --------------------------------------------------
# Calculator tool
# --------------------------------------------------

@agent.tool_plain
def calculate(
    operation: str,
    a: float,
    b: float,
) -> float:
    """
    Perform a mathematical calculation.
    """

    return calculator(
        operation,
        a,
        b,
    )


# --------------------------------------------------
# Weather tool
# --------------------------------------------------

@agent.tool_plain
def get_weather_tool(city: str) -> dict:
    """
    Get current weather for any city.

    Returns weather data on success or a readable error
    result if the location or weather cannot be retrieved.
    """

    return get_weather(city)


# --------------------------------------------------
# Web search tool
# --------------------------------------------------

@agent.tool_plain
def web_search_tool(question: str) -> str:
    """
    Search the web for current or up-to-date information.
    """

    return web_search(
        question,
        LLM_API_KEY,
        LLM_MODEL,
    )


# --------------------------------------------------
# Main application
# --------------------------------------------------

def main():

    print("================================")
    print("      AI STUDY ASSISTANT")
    print("================================")
    print("Type 'exit' to quit.")
    print()

    # Conversation memory
    message_history = []

    while True:

        question = input("You: ").strip()

        # Ignore empty input
        if not question:
            continue

        # Exit
        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:

            # Let PydanticAI and the LLM decide what to do
            result = agent.run_sync(
                question,
                message_history=message_history,
                model_settings={"timeout": 60},
            )

            # Save conversation history
            message_history = result.all_messages()

            # Display result
            print()
            print("AI:")
            print(f"Answer: {result.output.answer}")
            print(f"Topic: {result.output.topic}")
            print(f"Difficulty: {result.output.difficulty}")

            print(
                f"Used calculator: "
                f"{result.output.used_calculator}"
            )

            print(
                f"Used weather: "
                f"{result.output.used_weather}"
            )

            print(
                f"Used web search: "
                f"{result.output.used_web_search}"
            )

            print()

        except Exception as error:

            print()
            print("Something went wrong:")
            print(repr(error))
            print()


if __name__ == "__main__":
    main()