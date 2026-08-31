# 논문 노트 Front Matter 스키마

`vault/papers/` 아래 모든 노트 파일이 따라야 하는 표준 스키마 문서입니다.
템플릿은 [[../_templates/paper-note|_templates/paper-note.md]] 를 사용하세요.
파일명은 반드시 `<id>.md` 여야 합니다.

## 1. 필드 정의

| 필드 | 필수 | 타입 | 설명 |
|---|---|---|---|
| `id` | 필수 | 문자열 | vault 전체에서 유일한 kebab-case 식별자. 파일명과 동일해야 함 |
| `title` | 필수 | 문자열 | 논문 원문 제목 그대로 |
| `title_ko` | 선택 | 문자열 | 한글 요약 제목 |
| `authors` | 필수 | 리스트 | `"성, 이름"` 형식 (예: `"Fama, Eugene F."`) |
| `year` | 필수 | 정수 | 출판 연도 |
| `venue` | 선택 | 문자열 | 저널/학회명 |
| `doi` | 선택 | 문자열 | DOI |
| `source.drive_path` | 선택 | 문자열 | Google Drive 내 PDF 경로 (예: `IBK/papers/xxx.pdf`) |
| `source.drive_url` | 선택 | 문자열 | Drive 공유 링크 |
| `permission` | 필수 | enum | `public` \| `team` \| `private` (기본값 `private`) |
| `status` | 필수 | enum | `read` \| `skimmed` \| `to-verify` |
| `topics` | 필수 | 리스트 | 대주제, kebab-case |
| `keywords` | 필수 | 리스트 | 세부 키워드, kebab-case (그래프의 연결·군집 계산에 사용) |
| `methods` | 선택 | 리스트 | 방법론, kebab-case |
| `relations` | 선택 | 리스트 | 다른 노트와의 관계 (아래 §2) |
| `created` / `updated` | 필수 | 날짜 | `YYYY-MM-DD` |

### status 값의 의미

- `read` — 전체를 정독하고 수식·표까지 확인한 노트
- `skimmed` — 초록·서론·결론 중심으로 훑어본 노트
- `to-verify` — 일반 지식이나 2차 자료 기반으로 작성되어 원문 대조 검증이 필요한 노트

## 2. relation 5종과 사용 기준

각 relation 항목은 `type`, `target`(대상 노트 id), `note`(공개 가능 설명, 120자 이내),
`evidence`(비공개 원문 근거)를 가집니다. **근거(evidence) 없는 관계는 기록하지 않습니다.**

| type | 언제 쓰는가 |
|---|---|
| `supports` | 대상 논문의 핵심 주장·결론을 **실증적 또는 이론적으로 뒷받침**할 때. 단순히 인용만 한 경우에는 쓰지 않음 |
| `refutes` | 대상 논문의 주장·결과에 **정면으로 반하는 증거나 논리**를 제시할 때. 그래프에서 긴장(tension) 엣지로 시각화됨 |
| `extends` | 대상 논문의 **프레임·모형·데이터를 이어받아 확장·일반화**할 때 (예: 선형 요인모형 → 비선형 ML) |
| `same-method` | 결론과 무관하게 **동일하거나 매우 유사한 방법론**을 사용할 때 (예: 둘 다 OOS 예측회귀) |
| `shares-data` | **동일한 데이터셋 또는 그 파생 데이터**를 사용할 때 (예: 동일 특성(characteristics) 패널) |

- 한 쌍의 노트 사이에 여러 type을 동시에 기록할 수 있습니다 (예: `refutes` + `same-method`).
- `note`는 공개 그래프에 노출될 수 있으므로 민감한 내용을 담지 않습니다.
- `evidence`는 원문 인용 + 페이지 번호를 담으며 **절대 export되지 않습니다**.

## 3. permission 3단계와 export 규칙

| 값 | 의미 | 공개 그래프(graph.json) 포함 여부 |
|---|---|---|
| `public` | 완전 공개 가능 | 포함 |
| `team` | 팀 내부 공유용 | **기본 export에서 제외.** `build_graph.py --include-team` 을 명시했을 때만 포함 — 팀 내부 배포용으로만 사용하고, 세계 공개 저장소(IBK_public)에는 절대 사용하지 않습니다 |
| `private` | 개인 비공개 | **어떤 export에도 절대 포함되지 않음** |

**최소 컨텍스트 원칙 (minimal-context principle)**

공개 그래프로 나가는 정보는 오직 다음뿐입니다.

- 출처 메타데이터: `id`, `title`, `title_ko`, `year`, `source`(drive_path/drive_url/doi)
- 권한: `permission`, `status`
- 분류: `topics`, `keywords`, `methods`
- 관계: `relations`의 `type` / `target` / `note`(120자 절단)

다음은 **절대 export되지 않습니다**: 노트 본문 전체, 핵심 수식, 원문 인용(원문 근거 섹션),
relations의 `evidence` 필드, 그리고 `authors` · `venue` 필드. 그래프 export는
`scripts/build_graph.py` 를 통해서만 수행하며, 노트 본문을 IBK_public에 복사하는 행위는 금지입니다.

물리엔진 그래프 뷰어는 **탐색(exploration) 도구이지 진위 판단(truth-judgment) 도구가 아닙니다** —
엣지의 존재나 장력은 "여기를 읽어보라"는 신호일 뿐, 어느 논문이 옳다는 판정이 아닙니다.

## 4. kebab-case 규칙

`id`, `topics`, `keywords`, `methods` 에 적용됩니다.

- 소문자 영문자와 숫자만 사용, 단어 구분은 하이픈(`-`)
- 공백, 언더스코어, 대문자, 한글 금지 (예: `Factor Model` → `factor-model`)
- 약어도 소문자로 (예: `SDF` → `sdf`, `LDA` → `lda-topic-model`)
- 기존 vault에서 쓰인 키워드를 먼저 검색해 재사용하고, 동의어 난립을 피할 것
  (예: `neural-net` 와 `neural-networks` 를 혼용하지 않음)

## 5. id 명명 규칙

형식: `<firstauthor><year>-<short-slug>`

- `<firstauthor>` — 제1저자의 성(last name), 소문자 (예: `fama`, `gu`)
- `<year>` — 출판 연도 4자리 (예: `1993`, `2020`)
- `<short-slug>` — 논문 내용을 요약하는 2~4단어의 kebab-case 슬러그

예시:

- `fama1993-common-risk-factors`
- `gu2020-ml-asset-pricing`
- `welch2008-goyal-predictability` (공저자 성을 슬러그에 포함해 구분한 예)

동일 저자·연도의 논문이 여러 편이면 슬러그로 구분합니다. id는 한 번 부여하면
다른 노트의 `relations.target` 과 wikilink가 참조하므로 **변경하지 않는 것을 원칙**으로 합니다.
