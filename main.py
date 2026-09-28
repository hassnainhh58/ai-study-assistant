import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import StudyResponse
from tools import calculator, get_coordinates, get_weather


# Load variables from .env
load_dotenv()


# Read LLM configuration from environment variables
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")


if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY is missing from .env")

if not LLM_BASE_URL:
    raise ValueError("LLM_BASE_URL is missing from .env")

if not LLM_MODEL:
    raise ValueError("LLM_MODEL is missing from .env")


# Create the model through an OpenAI-compatible provider
model = OpenAIChatModel(
    LLM_MODEL,
    provider=OpenAIProvider(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
    ),
)


# Create the AI agent
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
    - weather questions

    You have access to two tools.

    1. Calculator:
       Use it when the user needs a mathematical calculation.

    2. Weather:
       Use it when the user asks about current weather.

    Decide yourself which tool is needed.

    Do not use the calculator for normal questions.

    Do not use the weather tool for normal questions.

    If the user asks about weather for a supported city,
    use the weather tool.

    Always return:
    - answer
    - topic
    - difficulty
    - used_calculator
    - used_weather
    """,
)


# Calculator tool
@agent.tool_plain
def calculate(
    operation: str,
    a: float,
    b: float,
) -> float:
    """
    Perform a mathematical calculation.
    """

    return calculator(operation, a, b)


# Weather tool
@agent.tool_plain
def weather(city: str) -> dict:
    """
    Get current weather for a city.
    """

    latitude, longitude = get_coordinates(city)

    return get_weather(latitude, longitude)


def main():
    print("================================")
    print("      AI STUDY ASSISTANT")
    print("================================")
    print("Type 'exit' to quit.")
    print()

    # Conversation memory
    message_history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = agent.run_sync(
                question,
                message_history=message_history,
            )

            # Save the conversation for the next turn
            message_history = result.all_messages()

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
            print()

        except Exception as error:
            print()
            print("Something went wrong:")
            print(error)
            print()


if __name__ == "__main__":
    main()