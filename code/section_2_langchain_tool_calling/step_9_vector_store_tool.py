import warnings

warnings.filterwarnings("ignore")

import re
from pprint import pprint
from langchain.document_loaders import TextLoader
from langchain_core.documents import Document


# 문서 분할 (Chunking)
def split_menu_items(document):
    """
    메뉴 항목을 분리하는 함수
    """
    # 정규표현식 정의
    pattern = r"(\d+\.\s.*?)(?=\n\n\d+\.|$)"
    menu_items = re.findall(pattern, document.page_content, re.DOTALL)

    # 각 메뉴 항목을 Document 객체로 변환
    menu_documents = []
    for i, item in enumerate(menu_items, 1):
        # 메뉴 이름 추출
        menu_name = item.split("\n")[0].split(".", 1)[1].strip()

        # 새로운 Document 객체 생성
        menu_doc = Document(
            page_content=item.strip(),
            metadata={
                "source": document.metadata["source"],
                "menu_number": i,
                "menu_name": menu_name,
            },
        )
        menu_documents.append(menu_doc)

    return menu_documents


# 메뉴판 텍스트 데이터를 로드
loader = TextLoader("../../data/restaurant_menu.txt", encoding="utf-8")
documents = loader.load()

print(len(documents))

# 메뉴 항목 분리 실행
menu_documents = []

for doc in documents:
    split_menu = split_menu_items(doc)

    menu_documents += split_menu

    # pprint(split_menu)
    # print("-" * 10)


# Chroma Vectorstore를 사용하기 위한 준비
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings_model = OllamaEmbeddings(model="bge-m3")

# # Chroma 인덱스 생성
# menu_db = Chroma.from_documents(
#     documents=menu_documents,
#     embedding=embeddings_model,
#     collection_name="restaurant_menu",
#     persist_directory="./chroma_db",
# )

# 벡터 저장소 로드
menu_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="restaurant_menu",
    persist_directory="./chroma_db",
)


# Retriever 생성
menu_retriever = menu_db.as_retriever(
    search_kwargs={"k": 2},
)

# 쿼리 테스트
query = "시그니처 스테이크의 가격과 특징은 무엇인가요?"
docs = menu_retriever.invoke(query)
print(f"검색 결과: {len(docs)}개")

for doc in docs:
    print(f"메뉴 번호: {doc.metadata['menu_number']}")
    print(f"메뉴 이름: {doc.metadata['menu_name']}")
    print()
