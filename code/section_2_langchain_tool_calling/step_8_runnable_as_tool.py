from textwrap import dedent
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from typing import List


# 도구 호출에 사용할 입력 스키마 정의
class SearchWikiSchema(BaseModel):
    """Input schema for Wikipedia search."""

    query: str = Field(..., description="The query to search for in Wikipedia")
    k: int = Field(2, description="The number of documents to return (default is 2)")


# WikipediaLoader를 사용하여 위키피디아 문서를 검색하는 함수
def search_wiki(input_data: dict) -> List[Document]:
    """Search Wikipedia documents based on user input (query) and return k documents"""

    query = input_data["query"]
    k = input_data.get("k", 2)

    wiki_loader = WikipediaLoader(query=query, load_max_docs=k, lang="ko")
    wiki_docs = wiki_loader.load()

    return wiki_docs


# RunnableLambda 함수를 사용하여 위키피디아 문서 로더를 Runnable로 변환
runnable = RunnableLambda(search_wiki)

wiki_search = runnable.as_tool(
    name="wiki_search",
    description=dedent(
        """
        Use this tool when you need to search for information on Wikipedia.
        It searches for Wikipedia articles related to the user's query and returns
        a specified number of documents. This tool is useful when general knowledge
        or background information is required.
    """
    ),
    args_schema=SearchWikiSchema,
)

# # 위키 검색 실행
# query = "국밥의 유래"
# wiki_results = wiki_search.invoke({"query": query})

# # # 검색 결과 출력
# for result in wiki_results:
#     print(result)

from pprint import pprint
from step_2_llm_model import llm
from step_6_custom_tool import search_web

llm_with_tools = llm.bind_tools(tools=[search_web, wiki_search])

query = "서울에서 가장 유명한 국밥집을 알려줘. 그리고 국밥의 유래에 대해서도 설명해줘."
result = llm_with_tools.invoke(query)

pprint(result)
print("-" * 100)
pprint(result.content)
print("-" * 100)
pprint(result.tool_calls)
