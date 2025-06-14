from typing import TypedDict


# 국내여행지 추천을 위한 상태값
class TravelRecommendationState(TypedDict):
    """
    국내여행지 추천을 위한 상태값
    """

    travel_type: str  # 여행 유형 (예: '도시', '문화', '자연', '등산', '바다', '역사')
    travel_location: str  # 여행지 위치 (예: '서울', '부산', '제주도')
    recommended_activities: list[str]  # 추천 활동 목록


def get_travel_location(state: TravelRecommendationState) -> TravelRecommendationState:
    """
    여행지 추천을 위한 상태값을 업데이트하는 함수
    """
    travel_type = state["travel_type"]

    if travel_type == "도시":
        state["travel_location"] = "서울"
    elif travel_type == "문화":
        state["travel_location"] = "경주"
    elif travel_type == "자연":
        state["travel_location"] = "제주도"
    elif travel_type == "등산":
        state["travel_location"] = "강원도"
    elif travel_type == "바다":
        state["travel_location"] = "부산"
    elif travel_type == "역사":
        state["travel_location"] = "경복궁"
    else:
        state["travel_location"] = "집에서 쉬기"

    return state


def get_recommended_activities(state: TravelRecommendationState) -> TravelRecommendationState:
    """
    여행지에 맞게 추천 활동 목록을 업데이트하는 함수
    """

    travel_location = state["travel_location"]

    if travel_location == "서울":
        state["recommended_activities"] = ["맛집 탐방", "관광지 방문", "공원 산책"]
    elif travel_location == "경주":
        state["recommended_activities"] = ["문화유산 탐방", "전통 음식 체험"]
    elif travel_location == "제주도":
        state["recommended_activities"] = ["해변 산책", "오름 등반", "제주 음식 체험"]
    elif travel_location == "강원도":
        state["recommended_activities"] = ["등산", "자연 탐방", "계곡 물놀이"]
    elif travel_location == "부산":
        state["recommended_activities"] = ["해운대 해수욕", "광안리 야경", "부산 먹거리 탐방"]
    elif travel_location == "경복궁":
        state["recommended_activities"] = ["궁궐 탐방", "전통 공연 관람"]
    else:
        state["recommended_activities"] = ["휴식", "독서", "영화 감상"]

    return state


from langgraph.graph import StateGraph, START, END

builder = StateGraph(TravelRecommendationState)

builder.add_node("get_travel_location", get_travel_location)
builder.add_node("get_recommended_activities", get_recommended_activities)

builder.add_edge(START, "get_travel_location")
builder.add_edge("get_travel_location", "get_recommended_activities")
builder.add_edge("get_recommended_activities", END)

graph = builder.compile()

# from IPython.display import Image, display

# # 그래프 시각화
# display(Image(graph.get_graph().draw_mermaid_png()))

# print(graph.get_graph().draw_mermaid())

answer = graph.invoke(
    {
        "travel_type": "관광",
    }
)

print("추천 여행지:", answer["travel_location"])
print("추천 활동 목록:", answer["recommended_activities"])


answer = graph.invoke(
    {
        "travel_type": "도시",
    }
)

print("추천 여행지:", answer["travel_location"])
print("추천 활동 목록:", answer["recommended_activities"])
