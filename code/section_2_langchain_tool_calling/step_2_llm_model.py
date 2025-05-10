from langchain_google_genai import ChatGoogleGenerativeAI
from step_1_tavily_search_tool import web_search

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

llm_with_tools = llm.bind_tools(tools=[web_search])
