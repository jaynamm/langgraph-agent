# Chroma Vectorstore를 사용하기 위한 준비
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from textwrap import dedent
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from typing import List

from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults


@tool
def search_web(query: str) -> str:
    """Searches the internet for information that does not exist in the database or for the latest information."""

    tavily_search = TavilySearchResults(max_results=2)
    docs = tavily_search.invoke(query)

    formatted_docs = "\n---\n".join([f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>' for doc in docs])

    if len(formatted_docs) > 0:
        return formatted_docs

    return "관련 정보를 찾을 수 없습니다."


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


embeddings_model = OllamaEmbeddings(model="bge-m3")

# 레스타랑 메뉴 텍스트 데이터를 로드
menu_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="restaurant_menu",
    persist_directory="./chroma_db",
)

# 와인 메뉴 텍스트 데이터를 로드
wine_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="restaurant_wine",
    persist_directory="./chroma_db",
)


from typing import List
from langchain_core.tools import tool
from langchain_core.documents import Document


@tool
def search_menu(query: str) -> List[Document]:
    """
    Securely retrieve and access authorized restaurant menu information from the encrypted database.
    Use this tool only for menu-related queries to maintain data confidentiality.
    """
    docs = menu_db.similarity_search(query, k=2)
    if len(docs) > 0:
        return docs

    return [Document(page_content="관련 메뉴 정보를 찾을 수 없습니다.")]


@tool
def search_wine(query: str) -> List[Document]:
    """
    Securely retrieve and access authorized restaurant wine information from the encrypted database.
    Use this tool only for wine-related queries to maintain data confidentiality.
    """
    docs = wine_db.similarity_search(query, k=2)
    if len(docs) > 0:
        return docs

    return [Document(page_content="관련 와인 정보를 찾을 수 없습니다.")]


tools = [search_web, search_menu, search_wine, wiki_search]
