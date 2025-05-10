from dotenv import find_dotenv, load_dotenv
import warnings

warnings.filterwarnings("ignore")

load_dotenv(find_dotenv())

from step_2_llm_model import llm_with_tools

# query = "안녕하세요."

# results = llm_with_tools.invoke(query)
# print(results)

# print(results.content)
# print(results.tool_calls)

query = "외국인들이 좋아하는 한국 음식을 알려주세요."

results = llm_with_tools.invoke(query)
print(results)

print(results.content)
print(results.tool_calls)

tool_call = results.tool_calls[0]
print(tool_call)
