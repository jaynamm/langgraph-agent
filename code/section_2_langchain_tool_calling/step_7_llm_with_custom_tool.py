import warnings

warnings.filterwarnings("ignore")

from pprint import pprint

from step_2_llm_model import llm
from step_6_custom_tool import search_web

llm_with_tools = llm.bind_tools(tools=[search_web])

query = "외국인들이 좋아하는 한국 음식을 알려주세요."
results = llm_with_tools.invoke(query)

# LLM의 전체 출력 결과 출력
pprint(results)
print("-" * 100)

# 메시지 content 속성 (텍스트 출력)
pprint(results.content)
print("-" * 100)

# LLM이 호출한 도구 정보 출력
pprint(results.tool_calls)
print("-" * 100)
