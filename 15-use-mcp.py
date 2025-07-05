import getpass
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# 환경 설정
load_dotenv(override=True)

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["./mcp/math_server.py"], 
                "transport": "stdio",
            },
            # 먼저 실행해두어야 한다.
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    
    tools = await client.get_tools()
    print("*** TOOLS : ", tools, "\n\n")
    
    # 에이전트 만들기 
    agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools
    )
    
    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    # )

    # print(math_response, "\n\n")

    # weather_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    # )

    # print(weather_response, "\n\n")

    while True:
        message = input("User: ")
        if message.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        response = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
        print("AI: "+response["messages"][-1].content, "\n\n")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    _set_env("TAVILY_API_KEY")
    _set_env("OPENAI_API_KEY")
    asyncio.run(main())
