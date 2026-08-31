---
id: gu2020-ml-asset-pricing
title: "Empirical Asset Pricing via Machine Learning"
title_ko: "머신러닝 기반 실증 자산가격결정"
authors:
  - "Gu, Shihao"
  - "Kelly, Bryan"
  - "Xiu, Dacheng"
year: 2020
venue: "Review of Financial Studies"
doi: "10.1093/rfs/hhaa009"
source:
  drive_path: "IBK/papers/gu_kelly_xiu_2020_ml_asset_pricing.pdf"
permission: public
status: to-verify
topics:
  - "asset-pricing"
  - "machine-learning-finance"
keywords:
  - "neural-networks"
  - "return-prediction"
  - "factor-model"
  - "feature-importance"
methods:
  - "neural-networks"
  - "random-forest"
  - "elastic-net"
relations:
  - type: extends
    target: fama1993-common-risk-factors
    note: "선형 요인모형 프레임을 고차원 특성 + 비선형 ML 예측함수로 일반화"
    evidence: "샘플 노트 — 원문 인용 생략 (실제 정독 시 서론의 요인모형 일반화 논의 페이지 인용)"
created: 2026-08-31
updated: 2026-08-31
---

# Empirical Asset Pricing via Machine Learning

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

개별 주식 수익률 예측 문제에 ML 방법론(벌점화 회귀·트리·신경망)을 대규모로 비교 적용해,
비선형 신경망이 전통적 선형 모형을 크게 능가하고 그 예측력이 경제적으로도 유의미함을 보였다.

## 핵심 주장

- 수익률 예측은 본질적으로 고차원·저신호 문제이며, 규제화(regularization)와 비선형성이 핵심이다.
- 얕은 신경망(NN3~NN4)이 OLS·벌점화 선형모형·트리 계열을 모두 능가한다.
- 예측력의 원천은 소수의 지배적 특성 — 모멘텀, 유동성, 변동성 계열 — 에 집중되어 있다.
- ML 예측 기반 포트폴리오는 거래비용 고려 전 기준으로 높은 샤프비율을 달성한다.

## 연구 방법

- 표본: 1957–2016년 미국 상장 주식 약 3만 종목, 월별 패널.
- 특성: 주식별 94개 특성 × 8개 거시 변수 상호작용 + 산업 더미 — 900개 이상의 예측 변수.
- 모형: OLS, elastic net, PCR, PLS, 일반화 선형모형, random forest, gradient boosting, 신경망(NN1–NN5).
- 검증: 시점 확장(recursive) 방식의 학습/검증/시험 분할로 순수 out-of-sample 성능 평가.

## 주요 결과

- 개별 주식 월별 OOS $R^2$: 신경망 계열 약 0.33~0.40%로 최고 (선형 OLS는 음수).
- 포트폴리오 수준 예측에서는 OOS $R^2$가 크게 상승 — 집계가 잡음을 상쇄.
- ML 예측 상하위 십분위 롱숏 포트폴리오의 가치가중 샤프비율이 시장 대비 2배 이상.
- 변수 중요도: 단기 반전, 모멘텀, 변동성, 유동성 특성이 상위권 — 모형 간 순위가 상당히 일치.

## 핵심 수식

$$
r_{i,t+1} = E_t[r_{i,t+1}] + \varepsilon_{i,t+1}, \qquad E_t[r_{i,t+1}] = g^{*}(z_{i,t})
$$

초과수익률의 조건부 기대를 특성 벡터 $z_{i,t}$의 유연한 함수 $g^{*}(\cdot)$로 두고, ML로 근사한다.

$$
R^2_{\mathrm{oos}} = 1 - \frac{\sum_{(i,t)\in\mathcal{T}} (r_{i,t+1} - \hat r_{i,t+1})^2}{\sum_{(i,t)\in\mathcal{T}} r_{i,t+1}^2}
$$

OOS 결정계수 — 벤치마크를 표본 평균이 아닌 0으로 두어(주식 프리미엄 과대평가 방지) 보수적으로 정의.

## 한계와 공백

- 거래비용·공매도 제약을 명시적으로 반영하지 않아 실현 가능한 초과수익은 불확실.
- 예측력의 상당 부분이 소형·비유동 종목에서 나올 가능성 — [[hou2020-replicating-anomalies]]의 미시총주 비판과 직결.
- 신경망의 해석 가능성 한계: 변수 중요도는 제공하나 경제적 메커니즘 규명은 미완.

## 참고문헌

- Fama & French (1993) — 선형 요인모형의 기준점 ([[fama1993-common-risk-factors]]).
- Welch & Goyal (2008) — OOS 예측 평가 프레임 ([[welch2008-goyal-predictability]]).
- Kozak, Nagel & Santosh (2020) — 수축 기반 SDF 접근 ([[kozak2020-shrinking-cross-section]]).

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 OOS R² 표와 변수 중요도 그림의 페이지를 인용할 것.)

## 연결 노트

- [[fama1993-common-risk-factors]] — extends: 선형 3요인 프레임을 고차원 특성·비선형 예측으로 일반화.
- 수신(incoming): [[kozak2020-shrinking-cross-section]] (supports, same-method),
  [[hou2020-replicating-anomalies]] (refutes), [[demo-private-internal-memo]] (shares-data).
