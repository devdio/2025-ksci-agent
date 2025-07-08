# AI 에이전트 모델 개발: Hands on 
**한국컴퓨터정보학회 2025 하계학술대회** 발표용이며, 발표 후 삭제될 예정입니다. 필요하신 분들은 다운로드 또는 Fork하시기 바랍니다.  


### 예제 내용 
코드는 LangCahin과 LangGraph로 구현되었습니다.  
  
1. 01-basic-chatbot.ipynb - LLM을 활용한 기본적인 Chatbot 구현
2. 02-add-tools.ipynb - 도구(Tool)호출을 위한 노드를 추가한 그래프 구현
3. 03-prebuilt-agent.ipynb - `create_react_agent`함수를 사용한 에이전트 구현
4. 04-supervisor-pattern.ipynb - 슈퍼바이저 패턴의 멀티에이전트 구현 
5. 05-prebuilt-create-supervisor.ipynb - 미리 구현된 `create_supervisor`함수 사용


### 환경 설정
작성된 예제는 OpenAI와 Tavily 서비스를 사용하고 있습니다. 예제를 실행하기 위해서는 OpenAI키와 Tavily서비스 Key가 필요합니다.
  
아래는 `.env`파일의 샘플입니다.
```
# OPENAI API KEY
OPENAI_API_KEY={your-api-key-here}

# LANGCHAIN TOOL
TAVILY_API_KEY={your-api-key-here}

# LANGSMITH 설정
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY={your-api-key-here}
LANGCHAIN_PROJECT={your-project-name-here}
LANGSMITH_API_KEY={your-api-key-here}
```

