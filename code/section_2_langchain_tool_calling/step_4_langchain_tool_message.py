from dotenv import find_dotenv, load_dotenv
import warnings

warnings.filterwarnings("ignore")

load_dotenv(find_dotenv())

from step_1_tavily_search_tool import web_search
from step_2_llm_model import llm_with_tools

query = "외국인들이 좋아하는 한국 음식을 알려주세요."

results = llm_with_tools.invoke(query)
print(results)

print(results.content)
print(results.tool_calls)

tool_call = results.tool_calls[0]
print(tool_call)

tool_output = web_search.invoke(tool_call["args"])

# print(tool_output)

# tool_message = web_search.invoke(tool_call)

# print(tool_message)

from langchain_core.messages import ToolMessage

tool_message = ToolMessage(
    content=tool_output,
    tool_call_id=tool_call["id"],
    name=tool_call["name"],
)

print(tool_message)
