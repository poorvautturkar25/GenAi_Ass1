from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
import os
from dotenv import load_dotenv

load_dotenv()

@wrap_model_call
def model_logging(request, handler):
    print("Before model call:", '-'*20)
    # print(request)
    response = handler(request)
    print("After model call: ", '-' * 20)
    # print (response)
    response.result[0].content = response.result[0].content.upper()
    return response

@wrap_model_call
def limit_model_context(request,handler):
    print("*Before model call:", '-'*20)
    # print(request)
    request = request.override(messages=request.messages[-5:])
    response = handler(request)
    print("*After model call:",'-'*20)
    # print(response)
    response.result[0].content = response.result[0].content.upper()
    return response

# create model 
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

# conversation context
conversation = []
# create agent
agent = create_agent(model=llm, 
            tools=[],
            middleware=[model_logging, limit_model_context],
            system_prompt="You are a helpful assistant. Answer in short."
        )

while True:
    # take user input
    user_input = input("You: ")
    if user_input == "exit":
        break
    # append user message in coversation
    conversation.append({"role": "user", "content": user_input})
    # invoke the agent
    result = agent.invoke({"messages": conversation})
    # print the result's last message
    ai_msg = result["messages"][-1]
    print("AI: ", ai_msg.content)
    # let's use conversation history returned by agent
    conversation = result["messages"]