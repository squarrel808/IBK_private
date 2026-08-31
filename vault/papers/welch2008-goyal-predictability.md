---
id: welch2008-goyal-predictability
title: "A Comprehensive Look at the Empirical Performance of Equity Premium Prediction"
title_ko: "주식 프리미엄 예측 변수들의 총체적 성과 검증"
authors:
  - "Welch, Ivo"
  - "Goyal, Amit"
year: 2008
venue: "Review of Financial Studies"
doi: "10.1093/rfs/hhm014"
source:
  drive_path: "IBK/papers/welch_goyal_2008_equity_premium.pdf"
permission: public
status: to-verify
topics:
  - "return-predictability"
keywords:
  - "equity-premium"
  - "out-of-sample"
  - "predictive-regression"
methods:
  - "predictive-regression"
  - "out-of-sample-tests"
created: 2026-08-31
updated: 2026-08-31
---

# A Comprehensive Look at the Empirical Performance of Equity Premium Prediction

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

배당수익률·이자율 스프레드 등 문헌의 대표적 주식 프리미엄 예측 변수들을 장기 표본에서 재검증해,
표본 외(OOS)에서는 대부분이 단순 역사적 평균조차 이기지 못하며 예측력이 불안정함을 보였다.

## 핵심 주장

- 표본 내(IS) 유의성은 표본 외(OOS) 예측력을 보장하지 않는다.
- 대부분의 예측 변수는 OOS에서 역사적 평균 벤치마크보다 나쁘다 ($R^2_{OOS} < 0$).
- 예측력이 있어 보이는 구간은 특정 시기(예: 오일쇼크)에 국한되며, 이후 표본에서는 소멸·역전된다.
- 실무자가 이 변수들로 시장 타이밍을 했다면 도움을 받지 못했을 것이다.

## 연구 방법

- 변수: 배당가격비율, 배당수익률, 주가수익비율, 장부가/시가, 국채수익률, 기간·부도 스프레드, 인플레이션 등 10여 개.
- 표본: 최장 1871년~2005년 연간·월간 데이터. 확장 창(expanding window) 방식의 재귀적 OOS 예측.
- 평가: OOS $R^2$, 누적 제곱예측오차 차이(ΔSSE) 그래프로 예측력의 시점별 안정성 진단.

## 주요 결과

- 대부분 변수의 $R^2_{OOS}$가 0 이하 — 역사적 평균이 사실상 최강 벤치마크.
- IS에서 유의했던 변수도 최근 30년 하위 표본에서는 예측력 상실.
- ΔSSE 그래프 진단: 예측 우위가 있더라도 소수 에피소드에 집중, 지속성 없음.
- 결론: "예측 변수들은 불안정하거나 이미 죽었다(unstable or spurious)".

## 핵심 수식

$$
r_{t+1} = \alpha + \beta x_t + \varepsilon_{t+1}
$$

표준 예측회귀 — 시점 $t$의 예측 변수 $x_t$로 다음 기 주식 프리미엄 $r_{t+1}$을 예측한다.

$$
R^2_{OOS} = 1 - \frac{\sum_{t}\left(r_t - \hat r_t\right)^2}{\sum_{t}\left(r_t - \bar r_t\right)^2}
$$

OOS 결정계수 — 벤치마크는 시점별 역사적 평균 $\bar r_t$. 음수이면 예측모형이 단순 평균보다 못함.

## 한계와 공백

- 개별 변수의 단변량 회귀 중심 — 변수 결합·제약 부과는 본격적으로 다루지 않음
  ([[campbell2008-thompson-predictability]]가 바로 이 지점을 공략).
- 선형 예측회귀에 국한 — 비선형·ML 접근의 여지.
- 통계적 예측력 부재가 곧 시변 기대수익률의 부재를 의미하는지는 해석의 여지.

## 참고문헌

- Campbell & Shiller (1988) — 배당가격비율 예측회귀의 고전.
- Goyal & Welch (2003) — 선행 논문 (배당비율 중심).
- Campbell & Thompson (2008) — 동일 호 게재된 반박 논문 ([[campbell2008-thompson-predictability]]).

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 변수별 IS/OOS R² 종합 표와 ΔSSE 그림 페이지를 인용할 것.)

## 연결 노트

- 발신(outgoing) 관계 없음.
- 수신(incoming): [[campbell2008-thompson-predictability]] (refutes, same-method) — 정면 반박 쌍으로,
  그래프에서 긴장(tension) 엣지 데모의 핵심 사례.
