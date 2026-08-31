# IBK_private — 논문 지식 vault 작업 지침

이 저장소는 **비공개** 논문 지식 vault입니다. 여기서 작업하는 Claude 세션의 역할은
**논문 PDF를 정독하고 표준화된 한국어 노트를 작성**하는 것입니다. 노트 작성은
`/paper-note` skill(`.claude/skills/paper-note/SKILL.md`)의 절차를 따르세요.

## 핵심 위치

- 노트 템플릿: `vault/_templates/paper-note.md`
- front matter 스키마 문서: `vault/_meta/schema.md` (필드 정의, relation 5종 사용 기준, permission·export 규칙, id 명명 규칙)
- 논문 노트: `vault/papers/<id>.md` — 파일명은 반드시 front matter의 `id`와 동일
- 토픽 허브(MOC): `vault/topics/` — 그래프에 export되지 않음, 사람용 지도

## 노트 작성 절차

1. PDF 전체를 정독한다 (수식·표 포함). 초록만 읽고 쓰지 않는다.
2. **기존 `vault/papers/` 전체의 front matter를 스캔**해 이미 쓰인 id·keywords·topics를 파악한다.
   - keywords는 기존 것을 재사용해 동의어 난립을 막는다.
   - relations의 `target`은 실존하는 노트 id만 가리켜야 한다.
3. 템플릿의 front matter와 본문 섹션 순서를 그대로 따라 노트를 작성한다.
4. relations는 **원문에서 근거를 확인한 것만** 기록하며, 각 관계에 `evidence`(인용 + 페이지)는 **필수**다.
   `note`는 공개 그래프에 노출될 수 있으므로 120자 이내, 민감 정보 금지.
5. 작성 후 반드시 `python3 scripts/validate_vault.py` 를 실행해 스키마 검증을 통과시킨다.
6. 관련 토픽 허브(`vault/topics/`)에 새 노트의 wikilink를 추가한다.

## permission 규칙

- 새 노트의 `permission`은 **항상 `private`로 시작**한다.
- `team` 또는 `public`으로의 상향은 **사용자의 명시적 승인이 있을 때만** 수행한다. 세션이 임의로 올리지 않는다.
- `private` 노트는 어떤 공개 export에도 포함되지 않는다.

## 절대 금지

- **vault 본문 내용(요약·수식·인용·evidence 포함)을 IBK_public 저장소에 복사하는 것.**
  공개 그래프로 나가는 정보는 최소 컨텍스트(출처 메타데이터·권한·topics/keywords/methods·relations의
  type/target/note)뿐이며, 그래프 export는 오직 `scripts/build_graph.py` 를 통해서만 수행한다.
  graph.json을 손으로 만들거나 본문을 붙여 넣는 방식의 export는 금지.
- relations에 근거(evidence) 없는 관계를 기록하는 것.
- 기존 노트의 `id`를 변경하는 것 (다른 노트의 target·wikilink가 깨진다).

## 참고

- 그래프 뷰어(IBK_public)는 탐색 도구이지 진위 판단 도구가 아니다 — refutes 엣지는
  "양쪽을 함께 읽으라"는 신호로만 서술한다.
- 사용자 대상 문서·노트는 한국어로 작성한다. 코드 식별자·주석은 영어여도 무방하다.
