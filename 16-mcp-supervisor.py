import getpass
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
import os
import asyncio
import asyncio.subprocess

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

async def main():
    model = ChatOpenAI(model_name="gpt-4o-mini")
    
    math_params = StdioServerParameters(
        command="python",
        args=["./mcp/math_server.py"],
    )

    time_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server_time"],
    )

    async with (
        stdio_client(math_params) as (math_read, math_write),
        stdio_client(time_params) as (time_read, time_write),
    ):
        async with (
            ClientSession(math_read, math_write) as math_session,
            ClientSession(time_read, time_write) as time_session,
        ):
            # 각 세션 초기화
            await math_session.initialize()
            await time_session.initialize()

            # 각 에이전트의 도구 취득 
            math_tools = await load_mcp_tools(math_session)
            time_tools = await load_mcp_tools(time_session)

            # 에이전트 구성 
            time_agent = create_react_agent(
                model=model,
                tools=time_tools,
                name="time_expert",
                prompt="주어진 곳의 현재 시간을 조사하는 전문가입니다."
            )
            math_agent = create_react_agent(
                model=model,
                tools=math_tools,
                name="math_expert",
                prompt="수학 계산을 진행하는 전문가입니다."
            )

            # 슈퍼바이저 작성 
            supervisor = create_supervisor(
                agents=[time_agent, math_agent],
                model=model,
                prompt=(
                    "당신은 팀 슈퍼바이저입니다.\n"
                    "- time_expert는 현재 시간을 확인하는 역할을 합니다\n"
                    "- math_expert는 수학적인 계산을하는 역할을 합니다\n"
                    "질문의 내용에 따라 적절한 전문가에게 분배해 주세요.\n"
                    "필요에 따라 여러 전문가에게 질문을 분배할 수도 있습니다."
                )
            ).compile()

            # # 메세지 이력을 표시 
            # response = await supervisor.ainvoke({
            #     "messages": [
            #         {
            #             "role": "user",
            #             "content": "부산의 현재 시간을 알려줘"
            #         }
            #     ]
            # })
                
            # for message in response["messages"]:
            #     if isinstance(message, AIMessage):
            #         print(message.content)
                    
            # -------------------------------------------------------------------------------
            # math_response = await agent.ainvoke(
            #     {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
            # )
        
            # print(math_response, "\n\n")
        
            # weather_response = await agent.ainvoke(
            #     {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
            # )
        
            # print(weather_response, "\n\n")
            # -------------------------------------------------------------------------------
            while True:
                message = input("User: ")
                if message.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                response = await supervisor.ainvoke({"messages": [{"role": "user", "content": message}]})
                print("AI: "+response["messages"][-1].content, "\n\n")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    load_dotenv(override=True)
    _set_env("TAVILY_API_KEY")
    _set_env("OPENAI_API_KEY")
    asyncio.run(main())
