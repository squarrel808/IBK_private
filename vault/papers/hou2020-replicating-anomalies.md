---
id: hou2020-replicating-anomalies
title: "Replicating Anomalies"
title_ko: "이상현상 재현 검증 — 복제 위기 진단"
authors:
  - "Hou, Kewei"
  - "Xue, Chen"
  - "Zhang, Lu"
year: 2020
venue: "Review of Financial Studies"
doi: "10.1093/rfs/hhy131"
source:
  drive_path: "IBK/papers/hou_xue_zhang_2020_replicating_anomalies.pdf"
permission: public
status: to-verify
topics:
  - "asset-pricing"
  - "replication"
keywords:
  - "anomalies"
  - "replication-crisis"
  - "microcaps"
  - "data-snooping"
methods:
  - "portfolio-sorts"
  - "replication"
relations:
  - type: refutes
    target: gu2020-ml-asset-pricing
    note: "미시총주 제외 시 다수 이상현상 소멸 — ML 예측력의 전제에 의문"
    evidence: "샘플 데모용 관계 — 원문은 GKX(2020)를 직접 다루지 않으므로(동시대 논문), 실제 정독 시 이 refutes 관계 자체의 존치 여부를 재검토할 것"
  - type: extends
    target: fama1993-common-risk-factors
    note: "요인·이상현상 문헌 전체를 대규모 재검증하며 FF 포트폴리오 정렬 프레임을 확장"
    evidence: "샘플 노트 — 원문 인용 생략 (실제 정독 시 방법론 절의 FF 프로토콜 준거 인용)"
created: 2026-08-31
updated: 2026-08-31
---

# Replicating Anomalies

> [!note] 이 노트는 파이프라인 데모용 샘플입니다. 실제 정독 노트로 교체하세요.

## 한 줄 요약

문헌에 보고된 400개 이상의 주식시장 이상현상을 통일된 절차로 재검증한 결과,
NYSE 분위점과 가치가중을 적용하면 약 3분의 2가 통계적 유의성을 잃는다는 것을 보였다.

## 핵심 주장

- 이상현상 문헌의 상당수는 미시총주(microcaps)의 과대 대표와 동일가중 정렬에 의존한 결과다.
- 미시총주는 종목 수로는 약 60%지만 시가총액으로는 3% 수준 — 경제적 대표성이 없다.
- 다중검정 기준(높은 t-임계값)을 적용하면 생존하는 이상현상은 더욱 줄어든다.
- 자산가격 연구에는 복제 위기(replication crisis)가 실재하며, 표준화된 재현 절차가 필요하다.

## 연구 방법

- 대상: 문헌에서 수집한 총 452개 이상현상 변수 (모멘텀, 가치·성장, 투자, 수익성, 무형자산, 거래마찰 등 6개 범주).
- 통일 절차: NYSE 시가총액 분위점, 가치가중 십분위 포트폴리오, 1967–2016년 공통 표본.
- 판정 기준: 상하위 십분위 롱숏 평균수익률의 |t| ≥ 1.96 (단일검정), |t| ≥ 2.78 (다중검정 보정).

## 주요 결과

- 452개 중 약 65%(재현 실패율)가 |t| < 1.96 — 원 논문의 유의성이 재현되지 않음.
- |t| ≥ 2.78 기준으로는 재현 실패율이 약 82%까지 상승.
- 거래마찰(trading frictions) 범주의 재현 실패율이 가장 높음 — 유동성 관련 변수 다수 소멸.
- 생존한 이상현상도 상당수는 q-요인 모형으로 설명 가능.

## 핵심 수식

$$
\bar{R}^{H-L} = \frac{1}{T}\sum_{t=1}^{T}\left(R^{High}_t - R^{Low}_t\right), \qquad
t = \frac{\bar{R}^{H-L}}{s(R^{H-L})/\sqrt{T}}
$$

상하위 십분위 롱숏 포트폴리오의 평균수익률과 t-통계량 — 재현 성공/실패 판정의 기본 통계량.

$$
|t| \ge 2.78
$$

다중검정(multiple testing)을 보정한 보수적 유의성 임계값 — 수백 개 변수를 동시에 검정할 때의 기준.

## 한계와 공백

- 가치가중·NYSE 분위점이 유일한 정답은 아니라는 반론 존재 — 소형주 정보를 버린다는 비판.
- 재현 실패가 곧 "효과 부재"의 증명은 아님 (검정력 문제) — 그래프에서 refutes 엣지를 탐색 신호로만 쓸 것.
- ML 기반 예측([[gu2020-ml-asset-pricing]])이 가치가중·대형주 유니버스에서 얼마나 살아남는지는 별도 검증 필요.

## 참고문헌

- Fama & French (1993) — 포트폴리오 정렬·요인 구성의 준거 ([[fama1993-common-risk-factors]]).
- Harvey, Liu & Zhu (2016) — 다중검정과 t-임계값 상향 제안.
- Hou, Xue & Zhang (2015) — q-요인 모형.

## 원문 근거

샘플 노트 — 원문 인용 생략. (실제 정독 시 범주별 재현 실패율 표와 미시총주 비중 통계 페이지를 인용할 것.)

## 연결 노트

- [[gu2020-ml-asset-pricing]] — refutes: 미시총주 제외 시 다수 이상현상 소멸 — ML 예측력의 데이터 전제에 의문.
- [[fama1993-common-risk-factors]] — extends: FF의 정렬·검정 프로토콜을 표준으로 삼아 문헌 전체를 재검증.
