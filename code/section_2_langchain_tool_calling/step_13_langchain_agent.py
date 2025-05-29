import warnings

warnings.filterwarnings("ignore")

from textwrap import dedent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            dedent(
                """
        You are an AI assistant providing restaurant menu information and general food-related knowledge. 
        Your main goal is to provide accurate information and effective recommendations to users.

        Key guidelines:
        1. For restaurant menu information, use the search_menu tool. This tool provides details on menu items, including prices, ingredients, and cooking methods.
        2. For general food information, history, and cultural background, utilize the wiki_summary tool.
        3. For wine recommendations or food and wine pairing information, use the search_wine tool.
        4. If additional web searches are needed or for the most up-to-date information, use the search_web tool.
        5. Provide clear and concise responses based on the search results.
        6. If a question is ambiguous or lacks necessary information, politely ask for clarification.
        7. Always maintain a helpful and professional tone.
        8. When providing menu information, describe in the order of price, main ingredients, and distinctive cooking methods.
        9. When making recommendations, briefly explain the reasons.
        10. Maintain a conversational, chatbot-like style in your final responses. Be friendly, engaging, and natural in your communication.


        Remember, understand the purpose of each tool accurately and use them in appropriate situations. 
        Combine the tools to provide the most comprehensive and accurate answers to user queries. 
        Always strive to provide the most current and accurate information.
        """
            ),
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Tool calling Agent 생성
from step_2_llm_model import llm
from langchain.agents import AgentExecutor, create_tool_calling_agent
from step_14_tools_group import tools

agent = create_tool_calling_agent(llm, tools, agent_prompt)

# AgentExecutor 생성
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# AgentExecutor 실행

query = "시그니처 스테이크의 가격과 특징은 무엇인가요? 그리고 스테이크와 어울리는 와인 추천도 해주세요."
agent_response = agent_executor.invoke({"input": query})

from pprint import pprint

pprint(agent_response)
