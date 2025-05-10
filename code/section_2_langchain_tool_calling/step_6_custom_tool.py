import warnings

warnings.filterwarnings("ignore")

from pprint import pprint
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Searches the internet for information that does not exist in the database or for the latest information."""

    tavily_search = TavilySearchResults(max_results=2)
    docs = tavily_search.invoke(query)

    formatted_docs = "\n---\n".join([f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>' for doc in docs])

    if len(formatted_docs) > 0:
        return formatted_docs

    return "관련 정보를 찾을 수 없습니다."


# 도구 속성
# print("자료형: ")
# print(type(search_web))
# print("-" * 100)

# print("name: ")
# print(search_web.name)
# print("-" * 100)

# print("description: ")
# pprint(search_web.description)
# print("-" * 100)

# print("schema: ")
# pprint(search_web.args_schema.schema())
# print("-" * 100)

# query = "스테이크와 어울리는 와인을 추천해주세요."
# search_result = search_web.invoke(query)

# print(search_result)
