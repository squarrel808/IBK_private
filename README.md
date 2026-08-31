# IBK_private — 논문 지식 Vault

논문 PDF를 정독해 표준화된 한국어 노트로 축적하고, 노트 사이의 관계(지지·반박·확장·동일방법·데이터공유)를
**최소 컨텍스트 그래프**로 추출해 공개 저장소(IBK_public)의 물리엔진 뷰어로 탐색하는 시스템의
**비공개 본체**입니다. 노트 본문·수식·인용·evidence는 이 저장소를 절대 떠나지 않습니다.

## 아키텍처 한 장 요약

```
Google Drive  (IBK/papers/*.pdf)
      │  ① 논문 PDF
      ▼
claude.ai/code 정독 세션  (/paper-note skill)
      │  ② 표준 한국어 노트 (front matter + 본문)
      ▼
IBK_private / vault/papers/*.md      ← 본문·수식·원문 인용·evidence (비공개 영역)
      │  ③ scripts/build_graph.py    ← 최소 컨텍스트만 추출 (출처·권한·키워드·제목·관계)
      ▼
graph.json                            ← private 노트는 완전 제외
      │  ④ 배포
      ▼
IBK_public  물리엔진(force-directed) 그래프 뷰어
             — 연결·보완·긴장(반박)·공백의 "탐색" 도구이지, 진위 판단 도구가 아님
```

## 디렉토리 구조

```
IBK_private/
├── CLAUDE.md                       # 이 저장소에서 작업하는 Claude 세션용 지침
├── README.md
├── .claude/
│   └── skills/paper-note/SKILL.md  # /paper-note skill (논문 정독 → 노트 작성 절차)
├── vault/
│   ├── _templates/paper-note.md    # 표준 노트 템플릿
│   ├── _meta/schema.md             # front matter 스키마·relation·permission·명명 규칙 문서
│   ├── papers/                     # 논문 노트 (<id>.md) — 그래프 노드의 원천, 유일한 스캔 대상
│   └── topics/                     # 토픽 허브(MOC) — export되지 않는 사람용 지도
├── scripts/                        # validate_vault.py, build_graph.py (별도 관리)
└── docs/                           # SETUP_WEB.md, WORKFLOW.md (별도 관리)
```

## 빠른 시작 (3단계)

1. **PDF 넣기** — 읽을 논문 PDF를 Google Drive의 `IBK/papers/` 폴더에 올립니다.
2. **정독 노트 만들기** — claude.ai/code 세션(이 저장소)에서 `/paper-note` 를 실행해
   노트를 작성하고, `python3 scripts/validate_vault.py` 로 스키마 검증을 통과시킵니다.
3. **그래프 내보내기** — `python3 scripts/build_graph.py` 로 `graph.json` 을 생성해
   IBK_public에 배포하면 뷰어에서 연결·긴장·공백을 탐색할 수 있습니다.

## 규칙 요약

- 새 노트의 `permission` 은 항상 `private` 로 시작하며, 상향(team/public)은 사용자 승인이 필요합니다.
- 공개 그래프로 나가는 것은 출처 메타데이터·권한·topics/keywords/methods·관계(type/target/note)뿐입니다.
  본문·수식·인용·evidence는 **절대** 나가지 않으며, export는 `scripts/build_graph.py` 로만 수행합니다.
- 상세 스키마와 relation 5종의 사용 기준은 `vault/_meta/schema.md` 를 참고하세요.

## 더 읽기

- [docs/SETUP_WEB.md](docs/SETUP_WEB.md) — claude.ai/code 웹 세션·Drive 커넥터 설정
- [docs/WORKFLOW.md](docs/WORKFLOW.md) — 정독 → 노트 → 검증 → export 전체 워크플로
