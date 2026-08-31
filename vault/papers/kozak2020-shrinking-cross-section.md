---
id: kozak2020-shrinking-cross-section
title: "Shrinking the Cross-Section"
title_ko: "횡단면의 수축 — 베이지안 SDF 추정"
authors:
  - "Kozak, Serhiy"
  - "Nagel, Stefan"
  - "Santosh, Shrihari"
year: 2020
venue: "Journal of Financial Economics"
doi: "10.1016/j.jfineco.2019.06.008"
source:
  drive_path: "IBK/papers/kozak_nagel_santosh_2020_shrinking.pdf"
permission: public
status: to-verify
topics:
  - "asset-pricing"
  - "machine-learning-finance"
keywords:
  - "sdf"
  - "shrinkage"
  - "bayesian"
  - "factor-model"
methods:
  - "bayesian-shrinkage"
  - "pca"
relations:
  - type: supports
    target: gu2020-ml-asset-pricing
    note: "고차원 특성 기반 예측에 규제화가 필수적이라는 결론을 SDF 관점에서 뒷받침"
    evidence: "샘플 노트 — 원문 인용 생략 (실제 정독 시 OOS 성과 비교 절 인용)"
  - type: same-method
    target: gu2020-ml-asset-pricing
    note: "고차원 특성 공간에서의 벌점화(수축) 추정이라는 공통 방법론"
    evidence: "샘플 노트 — 원문 인용 생략 (릿지형 벌점과 elastic net의 방법론적 대응 관계)"
created: 2026-08-31
updated: 2026-08-31
---

# Shrinking the Cross-Section

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

수십 개 특성 포트폴리오로 확률할인요인(SDF)을 추정할 때 경제적 사전분포에 기반한
베이지안 수축을 적용하면, 소수 특성의 희소(sparse) 모형보다 강건한 OOS 가격결정 성과를 얻음을 보였다.

## 핵심 주장

- 특성(characteristics) 공간에서 희소한 SDF — "요인 몇 개면 충분하다" — 는 데이터가 지지하지 않는다.
- 반면 주성분(PC) 공간에서는 소수의 큰 PC만으로 SDF를 근사할 수 있다 (PC 공간의 준희소성).
- 큰 고유값의 PC가 기대수익률 대부분을 설명해야 한다는 경제적 논리(차익거래 부재)를 사전분포로 번역할 수 있다.
- 이 수축 추정량은 릿지 회귀 형태가 되어 표본 평균수익률의 과적합을 억제한다.

## 연구 방법

- 데이터: 미국 주식의 50개 이상 특성 기반 롱숏 포트폴리오 수익률 (+ WFR 상호작용 확장 세트).
- SDF 계수에 대해 기대수익률이 공분산 구조(고유값)에 비례해야 한다는 사전분포를 부여.
- 사후 최빈 추정이 릿지형 폐형해로 도출되며, 벌점 강도는 교차검증으로 선택.
- 희소성 비교를 위해 L1(라쏘형) 벌점과 L2 벌점을 결합한 elastic-net형 추정도 수행.

## 주요 결과

- 특성 공간 희소 모형(예: 특성 3~5개)은 OOS에서 성과가 급락 — 어떤 소수 특성 조합도 충분하지 않음.
- PC 기반 수축 SDF는 OOS 횡단면 $R^2$와 샤프비율에서 일관되게 우수.
- 수축 강도를 높일수록 표본 내 성과는 희생되지만 OOS 성과가 개선 — 전형적 편의-분산 트레이드오프.
- 결론: "몇 개의 요인이면 충분한가"라는 질문 자체가 잘못 설정된 문제일 수 있음.

## 핵심 수식

$$
M_t = 1 - b^{\top}\left(F_t - \mathbb{E}[F_t]\right)
$$

특성 포트폴리오 수익률 $F_t$의 선형 결합으로 표현한 확률할인요인(SDF) — 계수 $b$의 추정이 핵심 문제.

$$
\hat{b} = \left(\Sigma + \gamma I\right)^{-1} \hat{\mu}
$$

베이지안 사전분포가 유도하는 릿지형 수축 추정량 — $\gamma$가 클수록 표본 평균 $\hat\mu$의 정보를 사전분포 쪽으로 수축.

## 한계와 공백

- 사전분포의 형태(고유값 감쇠 지수)가 결과에 미치는 민감도 — 대안적 사전분포 비교 여지.
- 선형 SDF에 국한 — 비선형 상호작용은 특성 확장으로만 부분 반영 ([[gu2020-ml-asset-pricing]]의 신경망과 대비).
- 특성 포트폴리오 구성 단계의 선택(가중, 리밸런싱)이 암묵적 전처리로 작용.

## 참고문헌

- Hansen & Jagannathan (1991) — SDF 분산 하한.
- Kozak, Nagel & Santosh (2018) — "Interpreting Factor Models" 선행 논문.
- Gu, Kelly & Xiu (2020) — ML 수익률 예측 ([[gu2020-ml-asset-pricing]]).

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 사전분포 유도 절과 OOS 성과 표 페이지를 인용할 것.)

## 연결 노트

- [[gu2020-ml-asset-pricing]] — supports: 고차원 규제화 접근의 우월성을 SDF 관점에서 지지.
- [[gu2020-ml-asset-pricing]] — same-method: 수축/벌점화 추정이라는 공통 방법론.
