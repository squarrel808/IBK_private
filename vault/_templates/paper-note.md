---
id: author2024-short-slug              # 필수. <제1저자성><연도>-<짧은-슬러그>, kebab-case, vault 전체에서 유일. 파일명은 반드시 <id>.md
title: "Original Paper Title"          # 필수. 원문 제목을 그대로 기입
title_ko: "한글 요약 제목"              # 선택. 한 눈에 내용이 파악되는 한국어 제목
authors:                               # 필수. "성, 이름" 형식의 리스트
  - "Last, First"
year: 2024                             # 필수. 출판 연도 (정수)
venue: "Journal Name"                  # 선택. 저널/학회/워킹페이퍼 시리즈명
doi: "10.xxxx/xxxx"                    # 선택. DOI가 있으면 기입
source:                                # 선택. 원문 PDF의 위치
  drive_path: "IBK/papers/filename.pdf"      # Google Drive 내 경로
  drive_url: "https://drive.google.com/..."  # Drive 공유 링크
permission: private                    # 필수. public | team | private. 기본값은 private, 상향은 사용자 승인 필요
status: to-verify                      # 필수. read(정독 완료) | skimmed(훑어봄) | to-verify(검증 필요)
topics:                                # 필수. 대주제 분류, kebab-case 리스트
  - "asset-pricing"
keywords:                              # 필수. 세부 키워드, kebab-case 리스트 (그래프 연결에 사용됨)
  - "factor-model"
methods:                               # 선택. 사용된 방법론, kebab-case 리스트
  - "ols-regression"
relations:                             # 선택. 원문 근거가 있는 관계만 기록
  - type: supports                     # supports | refutes | extends | same-method | shares-data
    target: other-note-id              # 대상 노트의 id (vault/papers/ 에 실존해야 함)
    note: "짧은 관계 설명 (공개 그래프에 노출될 수 있음, 120자 이내)"
    evidence: "원문 근거 인용 + 페이지 (비공개, 절대 export되지 않음)"
created: 2026-08-31                    # 노트 생성일 (YYYY-MM-DD)
updated: 2026-08-31                    # 마지막 수정일 (YYYY-MM-DD)
---

# Original Paper Title

## 한 줄 요약

논문 전체를 한 문장으로 압축한다 — 무엇을, 어떻게, 결론이 무엇인지.

## 핵심 주장

저자들이 주장하는 핵심 명제를 2~4개의 불릿으로 정리한다.

## 연구 방법

데이터(기간·표본·출처)와 방법론(모형·추정 방식·검정)을 구체적으로 기술한다.

## 주요 결과

정량적 수치(계수, R², t-통계량 등)를 포함해 주요 발견을 정리한다.

## 핵심 수식

논문의 핵심 수식을 $$ 블록의 LaTeX로 옮기고, 각 수식 아래에 한 줄 설명을 단다.

## 한계와 공백

저자가 인정한 한계 + 내가 판단한 공백(후속 연구 아이디어)을 구분해 적는다.

## 참고문헌

이 논문이 인용한 주요 문헌을 나열한다 (vault에 노트가 있으면 [[wikilink]]로).

## 원문 근거

핵심 주장을 뒷받침하는 원문 인용문과 페이지 번호를 적는다 — private 정보, 절대 export되지 않음.

## 연결 노트

front matter의 relations와 일치하는 [[other-id]] wikilink와 관계 설명을 나열한다.
