# 토픽 허브: 수익률 예측가능성 (return-predictability)

> [!info] 토픽 노트는 그래프에 노드로 export되지 않습니다 — build 스크립트는 `vault/papers/` 만 스캔합니다.
> 이 노트는 사람(그리고 정독 세션)이 문헌 지형을 조망하기 위한 MOC(Map of Content)입니다.

시장 전체(주식 프리미엄) 수준의 수익률을 표본 외(out-of-sample)에서 예측할 수 있는가를 다루는
축입니다. 이 vault에서 가장 선명한 **정면 반박 쌍(refutes pair)** 이 있는 곳으로, 물리엔진 그래프에서
긴장(tension) 엣지가 어떻게 보이는지 확인하기 좋은 영역입니다.

## 구성 논문

- [[welch2008-goyal-predictability]] — 대표 예측 변수 총검증: OOS에서는 역사적 평균조차 이기기 어렵다.
- [[campbell2008-thompson-predictability]] — 같은 프레임에 경제적 제약을 부과하면 예측력이 회복된다는 정면 반박.

## 논쟁 구조 메모

두 논문은 같은 데이터·같은 $R^2_{OOS}$ 지표를 쓰면서 (same-method) 정반대 결론에 도달합니다
(refutes). 쟁점은 "무제약 회귀의 추정 오차를 어디까지 이론으로 교정할 수 있는가"이며,
[[gu2020-ml-asset-pricing]]의 규제화 접근은 이 논쟁의 현대적 연장선으로 읽을 수 있습니다.
