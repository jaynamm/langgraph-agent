import warnings

warnings.filterwarnings("ignore")

from pprint import pprint
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from langchain_community.tools import TavilySearchResults

web_search = TavilySearchResults(max_results=2)

# query = "LangChain 에서 가장 자주 사용하는 도구는 무엇인가요?"

# search_results = web_search.invoke(query)

# for result in search_results:
#     print(result)
#     print("==========================")

# # 도구 속성
# print("자료형: ")
# print(type(web_search))
# print("-" * 100)

# print("name: ")
# print(web_search.name)
# print("-" * 100)

# print("description: ")
# pprint(web_search.description)
# print("-" * 100)

# print("schema: ")
# pprint(web_search.args_schema.schema())
# print("-" * 100)
