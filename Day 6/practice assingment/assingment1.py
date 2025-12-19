from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()



@tool
def calculator(expression):
    """
    This calculator function solves arithmetic expressions.
    Supports +, -, *, / and parentheses.
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"


@tool
def read_file(filepath):
    """
    Reads and returns the content of a local text file.
    """
    try:
        with open(filepath, "r") as file:
            text = file.read()
            return text
    except:
        return "Error: File not found"


@tool
def get_weather(city):
    """
    Returns current weather information of a city.
    """
    
    return f"The current weather in {city} is sunny with 30°C."


@tool
def knowledge_lookup(topic):
    """
    Returns basic knowledge about a topic.
    """
    data = {
        "python": "Python is a high-level programming language.",
        "langchain": "LangChain is a framework for LLM-based applications.",
        "groq": "Groq provides fast LLM inference."
    }
    return data.get(topic.lower(), "No information found.")




llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)




agent = create_agent(
    model=llm,
    tools=[
        calculator,
        read_file,
        get_weather,
        knowledge_lookup
    ],
    system_prompt="You are a helpful assistant. Answer in short."
)




def log_messages(messages):
    print("\n--- MESSAGE HISTORY ---")
    for msg in messages:
        print(msg)
    print("--- END ---\n")




conversation = []

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    conversation.append({"role": "user", "content": user_input})

    result = agent.invoke({
        "messages": conversation
    })

    conversation = result["messages"]

    log_messages(conversation)

    print("AI:", conversation[-1].content)