# 운영 워크플로 — 논문 1편 추가하기

구축([`docs/SETUP_WEB.md`](SETUP_WEB.md))이 끝난 상태를 전제로, 논문 한 편이
**PDF → 한국어 표준 노트 → 공개 그래프 → 물리엔진 뷰어**까지 흘러가는 표준 절차입니다.
전 과정이 브라우저(claude.ai/code, github.com)에서 이루어집니다.

```
[1] Drive 업로드 → [2] 정독 세션 → [3] 노트 작성·검증·푸시 → [4] PR 머지·자동 동기화 → [5] 뷰어 확인
```

---

## 1단계 — Drive IBK 폴더에 PDF 업로드

- Google Drive의 `IBK/papers/` 폴더에 PDF를 올립니다. 파일명은 `<year>-<slug>.pdf` 권장
  (예: `IBK/papers/2024-kelly-virtue-of-complexity.pdf`).
- 커넥터를 아직 연결하지 않았다면 이 단계는 건너뛰고, 2단계에서 PDF를 세션에 직접
  업로드하거나 Drive 공유 링크를 전달해도 됩니다.

## 2단계 — claude.ai/code에서 IBK_private 세션 시작

1. claude.ai/code → 새 세션 → 저장소 **`squarrel808/IBK_private`** 선택.
2. 모델은 **고성능 정독 모델(예: Opus 계열)** 로 선택합니다.
3. Google Drive 커넥터가 세션에 활성화되어 있는지 확인합니다.

프롬프트 예시 3가지:

> **예시 1 — Drive 커넥터가 연결된 경우 (기본)**
> ```
> /paper-note IBK/papers/2024-kelly-virtue-of-complexity.pdf 정독해서 노트 작성해줘
> ```

> **예시 2 — Drive 커넥터가 없어서 PDF를 세션에 직접 업로드한 경우**
> ```
> (PDF 파일을 입력창에 첨부한 뒤)
> 방금 업로드한 PDF를 /paper-note 절차대로 정독해서 vault 노트를 만들어줘.
> Drive에는 IBK/papers/2024-kelly-virtue-of-complexity.pdf 로 올려둘 예정이니
> source.drive_path 는 그 경로로 기록해줘.
> ```

> **예시 3 — 기존 노트와의 관계 탐색까지 요청하는 경우**
> ```
> /paper-note IBK/papers/2023-chen-deep-learning-hedging.pdf 정독해줘.
> 작성 후 vault/papers/ 의 기존 노트들과 supports/refutes/extends 관계 후보를
> 원문 근거(인용+페이지)와 함께 제안하고, 확실한 것만 relations에 넣어줘.
> ```

## 3단계 — 세션이 노트 작성 → 검증 → 커밋·푸시

세션은 `.claude/skills/paper-note/` 스킬 절차에 따라 다음을 수행합니다 (사용자는 결과만 검토):

1. PDF **전체 정독** (초록만 읽고 쓰지 않음 — 수식·표·각주 포함).
2. `vault/papers/<id>.md` 노트 작성 — front matter + 9개 본문 섹션,
   템플릿은 `vault/_templates/paper-note.md`, 규칙은 `vault/_meta/schema.md`.
3. 검증 실행:
   ```
   python3 scripts/validate_vault.py --vault vault/papers
   ```
   오류가 있으면 수정 후 재검증. (선택) 그래프 로직 회귀 확인:
   ```
   python3 scripts/test_build_graph.py
   ```
4. (선택) 로컬 미리보기 빌드로 export 결과 확인:
   ```
   python3 scripts/build_graph.py --vault vault/papers --out out/graph.json --pretty
   ```
   이 `out/graph.json` 에 본문·저자·evidence가 없는지 세션에게 확인시킬 수 있습니다.
5. 작업 브랜치에 커밋·푸시하고 PR 링크를 알려줍니다.

검토 포인트: **한 줄 요약이 원문과 맞는가, relations의 evidence가 실제 인용인가,
permission이 의도대로인가(기본 private)**.

## 4단계 — github.com에서 PR 확인·머지 → 공개 그래프 자동 갱신

1. 세션이 알려준 PR 링크(또는 `IBK_private` → Pull requests 탭)를 엽니다.
2. **Files changed** 에서 새 노트를 검토합니다. 특히:
   - `permission:` 값 (public/team이면 그래프에 노출됨 — 의도한 상향인지 확인)
   - relations의 `note:` (공개될 수 있음, 120자 이내) vs `evidence:` (비공개) 구분이 지켜졌는지
3. **Merge pull request** → **Confirm merge**.
4. 머지 즉시 **Actions 탭의 `sync-public` 워크플로**가 자동 실행됩니다:
   validate → build_graph → `IBK_public/data/graph.json` 커밋·푸시.
   초록색 체크를 확인하세요. 실패 시 로그에 한국어 오류 메시지가 남습니다.

## 5단계 — Pages 뷰어에서 확인

`https://squarrel808.github.io/IBK_public/` 를 열어 (Pages 반영까지 1~2분)
새 노드와 간선을 확인합니다. 뷰어 모드 4종:

| 모드 | 무엇을 보는가 |
|---|---|
| **기본** | 전체 그래프. 명시 관계 + 키워드 중첩 간선을 힘-방향 배치로 탐색 |
| **장력** | 각 간선을 스프링 변형률(현재 길이 vs 평형 길이)에 따라 색칠 — 이완은 파랑, 긴장은 빨강. 물리력 자체는 모든 모드에서 동일 |
| **충돌** | `refutes` 간선과 그 양 끝 노드만 강조하고 나머지는 흐리게 — 반박 쌍의 대치 구도를 골라 봄 |
| **공백** | 연결 1개 이하인 노드에 링 표시, 나머지는 흐리게 — 다음에 읽을 논문의 후보 지대 |

> 다시 강조: 뷰어는 **탐색 장치**입니다. "충돌" 모드가 보여주는 대치는 어느 쪽이 옳은지
> 말해주지 않습니다. 판단은 `IBK_private` 노트의 원문 근거로 돌아가서 하세요.

---

## relations 작성 가이드

관계는 그래프의 품질을 결정합니다. **원문에서 근거를 확인한 관계만** 기록합니다.

### 5가지 타입 판단 기준

| type | 이렇게 판단한다 | 예 |
|---|---|---|
| `supports` | 대상 논문의 **핵심 주장·결과를 재현하거나 뒷받침**하는 실증/이론 결과를 제시 | 다른 표본/기간에서 같은 프리미엄을 확인 |
| `refutes` | 대상 논문의 핵심 주장과 **양립 불가능한 결과**를 제시하거나 방법론적 결함을 직접 반박 | 같은 요인이 거래비용 반영 후 소멸함을 보임 |
| `extends` | 대상 논문의 **틀을 이어받아 확장/일반화** (새 자산군, 새 조건, 완화된 가정) | 주식 모형을 채권 시장으로 확장 |
| `same-method` | 주장 관계와 무관하게 **동일·거의 동일한 방법론**을 사용 | 둘 다 double machine learning 사용 |
| `shares-data` | **동일 데이터셋/데이터 소스**를 사용 (CRSP 같은 범용 DB는 표본·기간까지 겹칠 때만) | 동일한 옵션 패널 데이터 사용 |

판단 요령:

- `supports`/`refutes` 는 **핵심 주장** 단위로만 판단합니다. 각주 하나가 다르다고 refutes가 아닙니다.
- 헷갈리면 강한 주장을 피합니다: supports인지 extends인지 애매하면 `extends`,
  refutes인지 아닌지 애매하면 관계를 넣지 말고 노트 본문 `한계와 공백` 에 메모합니다.
- 방향: 새 노트가 기존 노트를 뒷받침하면 새 노트 front matter에 `target: <기존 id>` 로 적습니다.

### evidence 의무

- **모든 관계에는 `evidence`(원문 인용 + 페이지)가 필수**입니다. 예:
  ```yaml
  relations:
    - type: refutes
      target: gu2020-ml-asset-pricing
      note: "거래비용 반영 시 ML 포트폴리오 초과수익이 유의성을 잃음을 보임"
      evidence: "\"After transaction costs, the alpha becomes statistically indistinguishable from zero\" (p.23, Table 7)"
  ```
- `evidence` 는 **절대 export되지 않는** 비공개 필드입니다. 반대로 `note` 는 공개 그래프에
  노출될 수 있으므로 120자 이내로, 비공개 정보 없이 담백하게 씁니다.
- evidence를 채울 수 없는 관계는 관계가 아니라 **인상**입니다 — 기록하지 않습니다.

## permission 운영 원칙

- **기본값은 `private`** 입니다. 새 노트는 전부 private로 시작합니다 (스킬이 그렇게 작성함).
- private → team → public **상향은 반드시 명시적 결정**입니다: 노트를 다시 열어
  "이 논문의 존재·키워드·관계가 공개되어도 되는가"를 판단한 뒤 직접(또는 세션에 지시해서)
  `permission:` 을 수정하고 PR로 머지합니다. 자동 상향은 없습니다.
- 공개되는 것은 어차피 메타데이터뿐이지만, **어떤 논문을 읽고 어떻게 연결했는가 자체가
  연구 방향의 정보**입니다. 경쟁 감수성이 있는 주제는 private를 유지하세요.
- private 노트는 그래프에서 노드·간선 모두 제외되고 `counts.excluded_private` 숫자로만 남습니다.
- 하향(public → private)도 가능합니다: 값을 바꿔 머지하면 다음 동기화 때 그래프에서 사라집니다.

## 축적 후 로드맵

노트가 수십 편 쌓이면 다음 단계를 순서대로 도입할 만합니다.

1. **관계 자동 제안** — 정독 세션에 "vault 전체 front matter를 스캔해서 새 논문과의 관계 후보를
   evidence 후보와 함께 제안해줘"를 표준 절차화. 제안은 사람이 승인한 것만 relations에 반영.
2. **임베딩 유사도 보조 간선** — 현재의 keyword-overlap(자카드) 대신/병행하여 노트 요약의
   임베딩 코사인 유사도로 암묵 간선을 계산. 단, 최소 컨텍스트 원칙 유지 —
   임베딩 계산은 private 쪽에서 수행하고 공개 그래프에는 점수만 내보냄.
3. **반박 쌍 리뷰 세션** — 주기적으로 `refutes` 간선만 모아 정독 세션에서 양쪽 원문 근거를
   대조 검토: 정말 반박인가, 표본 차이인가, 조건부 성립인가. 결과는 양쪽 노트의
   `한계와 공백` 에 반영하고 필요 시 관계를 수정.
4. **공백 지대 독서 큐** — 뷰어의 "공백" 모드에서 발견한 빈 지대(연결이 성긴 토픽 쌍)를
   다음 논문 선정 기준으로 사용 — 그래프를 탐색 장치로 쓰는 본래 목적의 완성.
5. **토픽 허브 정비** — `vault/topics/` 허브 노트를 분기마다 재정리해 keywords 동의어를
   통합(kebab-case 표준화)하면 keyword-overlap 간선의 품질이 함께 올라갑니다.
