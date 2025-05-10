import warnings

warnings.filterwarnings("ignore")

from pprint import pprint
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from step_2_llm_model import llm_with_tools

today = datetime.today().strftime("%Y-%m-%d")

prompt = ChatPromptTemplate(
    [
        ("system", f"You are a helpful AI assistant. Today's date is {today}."),
        ("user", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)

llm_chain = prompt | llm_with_tools

from langchain_core.runnables import RunnableConfig, chain
from step_1_tavily_search_tool import web_search


@chain
def web_search_chain(user_input: str, config: RunnableConfig):
    _input = {"user_input": user_input}
    messages = llm_chain.invoke(_input, config=config)

    print("Message : ", messages)
    print("=====================")

    tool_messages = web_search.batch(messages.tool_calls, config=config)
    print("Tool Messages : ", tool_messages)
    print("=====================")

    return llm_chain.invoke(
        {
            **_input,
            "messages": [messages, *tool_messages],
        },
        config=config,
    )


response = web_search_chain.invoke("외국인들이 좋아하는 한국 음식을 알려주세요.")

pprint(response.content)
