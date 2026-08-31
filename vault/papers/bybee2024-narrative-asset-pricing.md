---
id: bybee2024-narrative-asset-pricing
title: "Business News and Business Cycles"
title_ko: "비즈니스 뉴스와 경기순환 — 내러티브 자산가격 연구"
authors:
  - "Bybee, Leland"
  - "Kelly, Bryan"
  - "Manela, Asaf"
  - "Xiu, Dacheng"
year: 2024
venue: "Journal of Finance"
source:
  drive_path: "IBK/papers/bybee_kelly_manela_xiu_business_news.pdf"
permission: public
status: to-verify
topics:
  - "text-analysis"
  - "macro-finance"
keywords:
  - "narrative"
  - "topic-model"
  - "news-data"
methods:
  - "lda-topic-model"
created: 2026-08-31
updated: 2026-08-31
---

# Business News and Business Cycles

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.
> 서지: Journal of Finance 2024년 게재본 기준. 워킹페이퍼(2020~)와 후속 내러티브 연구 계열을 포괄해 요약했다.

## 한 줄 요약

월스트리트저널 전문(全文) 기사에 LDA 토픽 모형을 적용해 "뉴스 주목도(attention)" 시계열을 추출하고,
이 내러티브 구조가 경기순환·거시 변수의 변동을 실시간으로 요약·예측함을 보인 내러티브 경제학 실증 연구 계열이다.

## 핵심 주장

- 뉴스 텍스트는 경제 상태에 대한 고차원 실시간 측정치이며, 토픽 구조로 압축할 수 있다.
- 특정 토픽(예: 경기침체, 금융위기 관련)에 대한 주목도가 산업생산·고용 등 거시 변수와 동행·선행한다.
- 뉴스 주목도는 기존 거시 지표가 담지 못하는 내러티브 정보(Shiller의 narrative economics)를 담는다.
- 텍스트 기반 상태변수는 자산가격(위험 프리미엄) 연구의 새로운 조건부 정보 집합이 될 수 있다.

## 연구 방법

- 데이터: Wall Street Journal 기사 전문, 1984년~2017년 수십만 건.
- 방법: 잠재 디리클레 할당(LDA)으로 약 180개 토픽 추정, 월별 뉴스 주목도 시계열 구성.
- 검증: 토픽 주목도와 거시 시계열의 동행성 분석, 거시 예측 회귀, 내러티브 사후 해석(레이블링).

## 주요 결과

- 소수의 토픽 주목도만으로 산업생산·실업률 변동의 상당 부분을 설명·요약.
- "recession" 계열 토픽 주목도가 경기 국면 전환 시점에 급등 — 실시간 경기 판단 지표로 기능.
- 토픽 구조는 시기별 지배 내러티브(닷컴, 금융위기, 무역분쟁 등)의 교체를 정량적으로 포착.
- 후속 계열 연구에서 뉴스 기반 요인의 자산가격 설명력을 추가 검증.

## 핵심 수식

$$
p(w \mid d) = \sum_{k=1}^{K} p(w \mid z = k)\; p(z = k \mid d)
$$

LDA의 생성 구조 — 문서 $d$의 단어 분포를 $K$개 토픽의 혼합으로 분해하며,
문서-토픽 비중 $\theta_{d,k} = p(z=k \mid d)$를 집계해 월별 뉴스 주목도 시계열을 만든다.

## 한계와 공백

- 단일 매체(WSJ) 의존 — 매체 편향과 편집 방침 변화가 토픽 시계열에 혼입될 수 있음.
- LDA 토픽 수·전처리 선택의 자의성, 토픽 레이블링의 사후 해석 위험.
- (vault 공백) 이 노트는 현재 의도적 고립 노드 — 텍스트 기반 상태변수와 수익률 예측 문헌
  (ML 자산가격, OOS 예측) 사이의 다리 관계가 아직 기록되지 않았다. 그래프 공백 탐색 데모용.

## 참고문헌

- Blei, Ng & Jordan (2003) — LDA 원 논문.
- Shiller (2017, 2019) — Narrative Economics.
- Gentzkow, Kelly & Taddy (2019) — Text as Data 서베이.

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 토픽-거시 동행성 표와 주목도 그림 페이지를 인용할 것.)

## 연결 노트

- 관계 없음 — **의도적 고립 노드**. 물리엔진 그래프에서 연결이 없는 노드가 어떻게 표류하며
  "여기와 기존 문헌 사이의 공백을 탐색하라"는 신호를 주는지 보여주는 데모.
