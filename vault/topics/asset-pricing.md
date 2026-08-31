# 토픽 허브: 자산가격결정 (asset-pricing)

> [!info] 토픽 노트는 그래프에 노드로 export되지 않습니다 — build 스크립트는 `vault/papers/` 만 스캔합니다.
> 이 노트는 사람(그리고 정독 세션)이 문헌 지형을 조망하기 위한 MOC(Map of Content)입니다.

자산의 기대수익률이 어떤 위험요인·특성으로 결정되는가를 다루는 축입니다. 이 vault에서는
고전적 선형 요인모형에서 출발해, ML 기반 고차원 예측과 그에 대한 재현성 비판까지의
논쟁 구조(extends / supports / refutes)를 따라가도록 구성되어 있습니다.

## 구성 논문

- [[fama1993-common-risk-factors]] — 3요인 모형의 원전. 이 축의 기준점(anchor) 노드.
- [[gu2020-ml-asset-pricing]] — 고차원 특성 + 비선형 ML로 요인 프레임을 일반화한 수익률 예측 연구.
- [[kozak2020-shrinking-cross-section]] — 베이지안 수축으로 SDF를 추정, "희소한 요인모형" 관념을 재검토.
- [[hou2020-replicating-anomalies]] — 이상현상 대규모 재검증. 미시총주·동일가중 의존성을 지적하며 ML 예측력의 전제에 긴장을 형성.

## 읽는 순서 제안

1. [[fama1993-common-risk-factors]] → 2. [[gu2020-ml-asset-pricing]] →
3. [[kozak2020-shrinking-cross-section]] (지지·동일방법) → 4. [[hou2020-replicating-anomalies]] (반박 축).
refutes 엣지는 진위 판정이 아니라 "양쪽을 함께 읽으라"는 탐색 신호로 사용하세요.
