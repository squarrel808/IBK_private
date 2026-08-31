---
name: paper-note
description: 논문 PDF를 정독하여 IBK_private vault의 표준 한국어 논문 노트(front matter + 9개 본문 섹션)를 작성합니다. 사용자가 "논문 정독", "노트 작성", "paper-note"를 요청하거나 PDF를 주며 vault에 넣어달라고 할 때 사용하세요.
---

# /paper-note — 논문 정독 → 표준 노트 작성

논문 한 편을 정독해 `vault/papers/<id>.md` 표준 노트를 만드는 절차입니다.
템플릿은 `vault/_templates/paper-note.md`, 스키마 규칙은 `vault/_meta/schema.md` 를 따릅니다.

## 절차

### 1. PDF 확보

- **Google Drive 커넥터가 연결된 세션이면**: 커넥터 도구로 Drive의 `IBK` 폴더에서 해당 논문을
  검색·열람한다. front matter의 `source.drive_path` / `source.drive_url` 에 위치를 기록한다.
- **커넥터가 없으면**: 세션에 업로드된 PDF, 또는 사용자가 지정한 로컬 경로의 PDF를 사용한다.
- 어느 쪽도 없으면 사용자에게 PDF 위치를 물어본다. 원문 없이 기억만으로 쓰지 않는다.

### 2. 전체 정독

- 초록·서론만 읽고 쓰지 않는다. **수식·표·각주까지 전체를 정독**한다.
- 핵심 주장별로 나중에 `원문 근거` 섹션과 relations의 `evidence`에 넣을 인용문·페이지를 수집한다.

### 3. 기존 vault 스캔

- `vault/papers/` 전체의 front matter에서 기존 `id`, `keywords`, `topics`, `methods` 를 스캔한다.
- keywords는 기존 표기를 재사용한다 (동의어 신설 금지, kebab-case).
- 이 논문과 기존 노트 사이의 관계 후보(supports / refutes / extends / same-method / shares-data)를 찾는다.

### 4. 노트 작성

- id는 `<firstauthor><year>-<short-slug>` 형식, 파일명은 `<id>.md`.
- 템플릿의 front matter와 본문 섹션(한 줄 요약 ~ 연결 노트)을 순서 그대로 모두 채운다.
- `핵심 수식`은 $$ LaTeX 블록 + 수식별 한 줄 설명.
- **relations는 원문에서 근거를 확인한 것만** 기록하고, 각 관계의 `evidence`(인용 + 페이지)는 필수.
  `note`는 공개될 수 있으므로 120자 이내로 담백하게.
- 새 노트의 `permission`은 **private로 시작**한다 (상향은 사용자 승인 필요).
- 관련 토픽 허브(`vault/topics/`)에 wikilink를 추가한다.

### 5. 검증

```bash
python3 scripts/validate_vault.py
```

통과할 때까지 스키마 오류(필수 필드 누락, kebab-case 위반, 존재하지 않는 target 등)를 수정한다.

### 6. 요약 보고

사용자에게 다음을 보고한다: 생성한 노트 id와 경로, status(read/skimmed/to-verify),
기록한 relations와 그 근거 요지, 검증 결과, permission 상태(private) 및 상향 여부 질문.
