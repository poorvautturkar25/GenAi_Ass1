from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

# create model
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider= "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# convsersation context
conversation = []
#create agent
agent = create_agent(model=llm,
                     tools=[],
                     system_prompt="You ar ea helpful assistant.Answer in short."
                     )
while True:
    #take user input
    user_input = input("You:")
    if user_input == "exit":
        break
    #append user message in conversation
    conversation.append({"role": "user", "content": user_input})
    #invoke the agent 
    result = agent.invoke({"messages": conversation})
    #print th result's last message
    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)
    # let's use conberation history returned by agent
    conversation = result["messages"]

