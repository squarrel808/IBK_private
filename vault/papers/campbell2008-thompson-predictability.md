---
id: campbell2008-thompson-predictability
title: "Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?"
title_ko: "표본 외 초과수익률 예측 — 역사적 평균을 이길 수 있는가"
authors:
  - "Campbell, John Y."
  - "Thompson, Samuel B."
year: 2008
venue: "Review of Financial Studies"
doi: "10.1093/rfs/hhm055"
source:
  drive_path: "IBK/papers/campbell_thompson_2008_predicting_oos.pdf"
permission: public
status: to-verify
topics:
  - "return-predictability"
keywords:
  - "equity-premium"
  - "out-of-sample"
  - "economic-restrictions"
  - "predictive-regression"
methods:
  - "predictive-regression"
  - "out-of-sample-tests"
relations:
  - type: refutes
    target: welch2008-goyal-predictability
    note: "계수 제약 부과 시 예측력 회복 — 정면 반박 쌍"
    evidence: "샘플 노트 — 원문 인용 생략 (실제 정독 시 제약 전후 OOS R² 비교 표 인용)"
  - type: same-method
    target: welch2008-goyal-predictability
    note: "동일한 OOS 예측회귀 프레임과 R2-OOS 지표를 사용"
    evidence: "샘플 노트 — 원문 인용 생략 (동일 벤치마크·동일 평가 지표 사용 명시 부분)"
created: 2026-08-31
updated: 2026-08-31
---

# Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

예측회귀에 이론이 시사하는 부호 제약과 프리미엄 비음(非陰) 제약을 부과하면 다수 변수의
OOS 예측력이 회복되며, 작은 $R^2_{OOS}$도 투자자에게 경제적으로 유의미할 수 있음을 보였다.

## 핵심 주장

- Welch–Goyal의 OOS 실패는 무제약 회귀의 추정 오차 탓이 크다 — 경제 이론이 주는 약한 제약으로 상당 부분 교정된다.
- 제약 (1): 예측 계수의 부호가 이론과 반대이면 0으로 설정. 제약 (2): 프리미엄 예측치가 음수이면 0으로 절단.
- 제약 부과 후 다수 가치평가 비율 변수의 $R^2_{OOS}$가 양수로 전환.
- 월간 0.5% 수준의 작은 $R^2$도 시장 샤프비율 제곱과 비교하면 무시할 수 없는 효용 이득을 준다.

## 연구 방법

- Welch–Goyal과 동일한 변수·표본·재귀적 OOS 프레임을 채택해 직접 비교 가능성을 확보.
- 무제약 회귀 vs 부호 제약 vs 예측치 절단 vs 이론 기반 정률(스티어드) 예측을 단계적으로 비교.
- 평균-분산 투자자의 포트폴리오 선택 문제로 예측력의 경제적 가치를 환산.

## 주요 결과

- 무제약 회귀는 Welch–Goyal 결과를 재확인 — 대부분 $R^2_{OOS} < 0$.
- 두 가지 제약 부과 후 배당수익률·수익수익률(earnings yield) 등에서 $R^2_{OOS} > 0$ 달성.
- 월간 $R^2_{OOS} \approx 0.43\%$ 수준이면 위험회피 계수 3의 투자자에게 의미 있는 수익률 개선.
- 결론: "역사적 평균을 이길 수 있다 — 단, 이론적 제약과 겸손한 기대 하에서".

## 핵심 수식

$$
\tilde\beta_t =
\begin{cases}
0, & \hat\beta_t \text{의 부호가 이론과 반대일 때} \\
\hat\beta_t, & \text{그 외}
\end{cases}
\qquad
\hat r_{t+1} = \max\!\bigl(0,\; \hat\alpha_t + \tilde\beta_t x_t\bigr)
$$

경제적 제약 두 규칙 — (1) 이론과 반대 부호의 **계수**를 0으로 두면 예측치는 절편(대략 역사적 평균)으로 회귀하고, (2) 그래도 음수인 프리미엄 **예측치**는 0으로 절단한다.

$$
\frac{\Delta \mathbb{E}[r_p]}{\mathbb{E}[r_p]} \approx \frac{R^2_{OOS}}{S^2}
$$

예측력의 경제적 가치 — 기대수익률의 비례적 개선은 $R^2_{OOS}$를 시장 샤프비율 제곱 $S^2$과 비교해 평가해야 함.

## 한계와 공백

- 제약 자체가 일종의 사후 정보라는 비판 가능 — 어떤 제약을 "이론적"으로 인정할지의 경계 문제.
- 예측 이득이 표본·기간에 따라 여전히 불안정 — 논쟁은 완전히 종결되지 않음.
- 단변량 프레임 유지 — 다변량 수축 접근([[kozak2020-shrinking-cross-section]] 류)과의 결합은 후속 과제.

## 참고문헌

- Welch & Goyal (2008) — 직접 반박 대상 ([[welch2008-goyal-predictability]]).
- Campbell (1987), Campbell & Shiller (1988) — 예측회귀의 이론적 배경.
- Merton (1980) — 기대수익률 추정의 어려움.

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 제약 전후 R²_OOS 비교 표와 효용 환산 절 페이지를 인용할 것.)

## 연결 노트

- [[welch2008-goyal-predictability]] — refutes: 계수 제약 부과 시 예측력 회복 — 정면 반박 쌍
  (그래프 긴장 엣지 데모의 핵심 사례).
- [[welch2008-goyal-predictability]] — same-method: 동일한 OOS 예측회귀 프레임과 $R^2_{OOS}$ 지표 사용.
