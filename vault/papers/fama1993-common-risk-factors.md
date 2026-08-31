---
id: fama1993-common-risk-factors
title: "Common Risk Factors in the Returns on Stocks and Bonds"
title_ko: "주식·채권 수익률의 공통 위험요인 (3요인 모형)"
authors:
  - "Fama, Eugene F."
  - "French, Kenneth R."
year: 1993
venue: "Journal of Financial Economics"
doi: "10.1016/0304-405X(93)90023-5"
source:
  drive_path: "IBK/papers/fama_french_1993_common_risk_factors.pdf"
permission: public
status: to-verify
topics:
  - "asset-pricing"
  - "factor-models"
keywords:
  - "factor-model"
  - "three-factor-model"
  - "size-effect"
  - "value-effect"
  - "risk-premium"
methods:
  - "time-series-regression"
  - "portfolio-sorts"
created: 2026-08-31
updated: 2026-08-31
---

# Common Risk Factors in the Returns on Stocks and Bonds

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

시장 초과수익률에 규모(SMB)·가치(HML) 요인을 더한 3요인이 주식 수익률의 횡단면 변동을,
만기(TERM)·부도(DEF) 요인이 채권 수익률을 대부분 설명함을 시계열 회귀로 보였다.

## 핵심 주장

- CAPM의 시장 베타만으로는 규모·가치 프리미엄을 설명할 수 없다.
- 규모(SMB)와 장부가/시가 비율(HML)을 모방하는 포트폴리오 수익률이 주식의 공통 위험요인을 포착한다.
- 채권에는 만기 프리미엄(TERM)과 부도 프리미엄(DEF) 두 요인이 작동하며, 주식·채권 시장은 요인을 통해 연결된다.
- 3요인 회귀의 절편(알파)이 대체로 0에 가까워, 요인들이 기대수익률의 횡단면을 잘 설명한다.

## 연구 방법

- 표본: 1963–1991년 NYSE/AMEX/NASDAQ 주식과 미 국채·회사채 월별 수익률.
- 규모(2분위)×장부가/시가(3분위) 독립 이중 정렬로 6개 포트폴리오를 만들어 SMB, HML 요인을 구성.
- 검정 자산: 규모×B/M 5×5 = 25개 포트폴리오. 요인 수익률에 대한 시계열 OLS 회귀로 절편(알파)을 검정.

## 주요 결과

- 시장 단일요인 회귀에서는 소형·가치 포트폴리오의 알파가 크게 유의하지만, 3요인 회귀에서는 대부분 소멸.
- 25개 포트폴리오에 대한 3요인 회귀의 R²가 대체로 0.9 이상.
- SMB·HML 기울기가 규모·B/M 특성에 따라 체계적으로 변화 — 요인 로딩이 특성 정보를 흡수.
- 채권 수익률은 TERM·DEF로 잘 설명되며, 주식 요인의 추가 설명력은 제한적.

## 핵심 수식

$$
R_{it} - R_{Ft} = a_i + b_i\,(R_{Mt} - R_{Ft}) + s_i\,\mathrm{SMB}_t + h_i\,\mathrm{HML}_t + e_{it}
$$

3요인 시계열 회귀 — 절편 $a_i$가 0이면 요인들이 포트폴리오 $i$의 기대 초과수익률을 완전히 설명한다.

$$
\mathrm{SMB}_t = \tfrac{1}{3}(SL + SM + SH)_t - \tfrac{1}{3}(BL + BM + BH)_t
$$

규모 요인 — 소형(S) 3개 포트폴리오 평균수익률에서 대형(B) 3개 포트폴리오 평균수익률을 뺀 모방 포트폴리오.

## 한계와 공백

- (저자 인정) SMB·HML이 어떤 경제적 위험을 대변하는지에 대한 이론적 근거는 제시하지 않음 — 실증적 구성물.
- 데이터 스누핑 가능성: 정렬 변수 자체가 표본 내 이상현상에서 출발했다는 비판 (후속 논쟁의 출발점).
- 모멘텀 등 3요인이 설명하지 못하는 이상현상이 이후 다수 보고됨 — 요인 추가 경쟁의 시초.

## 참고문헌

- Fama & French (1992), "The Cross-Section of Expected Stock Returns" — 횡단면 선행 연구.
- Banz (1981) — 규모 효과 최초 보고.
- Chen, Roll & Ross (1986) — 거시 요인 접근.

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 핵심 주장별 인용문과 페이지를 기입할 것.)

## 연결 노트

- 발신(outgoing) 관계 없음 — 이 vault에서 여러 후속 연구의 기준점(anchor) 노드 역할.
- 수신(incoming): [[gu2020-ml-asset-pricing]] (extends), [[hou2020-replicating-anomalies]] (extends).
