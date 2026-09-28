# AI Study Assistant

An AI-powered study assistant built with Python and PydanticAI.

The project demonstrates how an LLM can understand a user's question, decide whether a tool is required, call the appropriate Python tool, and return a structured response.

## Features

* AI-powered question answering
* Calculator tool for mathematical calculations
* Weather tool for current weather information
* Structured output using Pydantic
* Conversation history during the current application session
* OpenRouter integration using an OpenAI-compatible API
* Current model configured through environment variables

## Technologies Used

* Python
* PydanticAI
* Pydantic
* OpenRouter
* Grok LLM
* HTTPX
* Open-Meteo Weather API
* python-dotenv

## Project Structure

```text
aiassistant/
│
├── .gitignore
├── main.py
├── models.py
├── tools.py
└── README.md
```

The following files are intentionally not included in the repository:

```text
.venv/
.env
__pycache__/
*.pyc
```

These contain local environment files, secrets, or Python-generated files.

## How the Project Works

The general flow is:

```text
User
  ↓
PydanticAI Agent
  ↓
LLM
  ↓
Decides whether a tool is required
  ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
No Tool       Calculator       Weather
 ↓               ↓               ↓
Direct        Python          Python
Answer        Function        Function
                ↓               ↓
              Result          Open-Meteo
                └───────┬───────┘
                        ↓
                       LLM
                        ↓
               Structured Output
                        ↓
                    Pydantic
                        ↓
                     User
```

The LLM decides which action is required, PydanticAI orchestrates the interaction, and Python executes the registered tools.

## Available Tools

### Calculator

The calculator tool performs basic mathematical operations such as:

* Addition
* Subtraction
* Multiplication
* Division

Example:

```text
What is 25 multiplied by 8?
```

The LLM can decide that the calculator tool is required and provide the appropriate arguments to the Python function.

### Weather

The weather tool accepts a supported city and retrieves current weather information.

The current implementation uses city coordinates and sends an HTTP request to the Open-Meteo API.

Example:

```text
What is the weather in Islamabad?
```

## Structured Output

The application uses a Pydantic model named `StudyResponse`.

The response contains:

```text
answer
topic
difficulty
used_calculator
used_weather
```

This provides a predictable structure for the application's final output.

## Conversation Memory

The application maintains conversation history using PydanticAI message history.

During a running session:

```text
User message
     ↓
Agent
     ↓
Result
     ↓
Message history updated
     ↓
Next user message
     ↓
Previous conversation + new message
```

The current implementation provides **session-based conversation memory**.

The history is stored while the Python application is running. Restarting the application clears the current conversation history.

## Environment Variables

The project uses a `.env` file for configuration.

Example:

```text
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=your_model_name
```

The actual `.env` file is intentionally excluded from GitHub through `.gitignore`.

Never commit API keys or other secrets to the repository.

## Installation

Create and activate a virtual environment:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Install the required packages:

```cmd
pip install pydantic-ai python-dotenv httpx
```

## Running the Project

From the project directory:

```cmd
python main.py
```

The application starts an interactive conversation.

Example:

```text
You: What is 25 multiplied by 8?

AI:
Answer: 25 multiplied by 8 is 200.
```

To exit:

```text
exit
```

## Project Purpose

This project was created as a practical learning project for understanding:

* Python application structure
* LLM integration
* PydanticAI agents
* Tool calling
* Python functions as AI tools
* API requests
* Structured outputs
* Conversation history
* Agentic AI workflows
