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


# Chroma Vectorstore를 사용하기 위한 준비
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings_model = OllamaEmbeddings(model="bge-m3")

# 와인 메뉴 텍스트 데이터를 로드
loader = TextLoader("../../data/restaurant_wine.txt", encoding="utf-8")
documents = loader.load()

# 메뉴 항목 분리 실행
menu_documents = []
for doc in documents:
    menu_documents += split_menu_items(doc)

# 결과 출력
print(f"총 {len(menu_documents)}개의 메뉴 항목이 처리되었습니다.")
for doc in menu_documents[:2]:
    print(f"\n메뉴 번호: {doc.metadata['menu_number']}")
    print(f"메뉴 이름: {doc.metadata['menu_name']}")
    print(f"내용:\n{doc.page_content[:100]}...")


# Chroma 인덱스 생성
wine_db = Chroma.from_documents(
    documents=menu_documents,
    embedding=embeddings_model,
    collection_name="restaurant_wine",
    persist_directory="./chroma_db",
)

wine_retriever = wine_db.as_retriever(
    search_kwargs={"k": 2},
)

query = "스테이크와 어울리는 와인을 추천해주세요."
docs = wine_retriever.invoke(query)
print(f"검색 결과: {len(docs)}개")

for doc in docs:
    print(f"메뉴 번호: {doc.metadata['menu_number']}")
    print(f"메뉴 이름: {doc.metadata['menu_name']}")
    print()
