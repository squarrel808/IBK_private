#!/usr/bin/env bash
# 비공개 vault를 검증하고 최소 컨텍스트 graph.json을 빌드한 뒤,
# 로컬 IBK_public 체크아웃의 data/graph.json 으로 복사하는 편의 스크립트.
#
# 사용법: scripts/export_to_public.sh [IBK_public 경로]
#   기본값: ../IBK_public (IBK_private 저장소 루트 기준)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PUBLIC_DIR="${1:-$ROOT_DIR/../IBK_public}"
OUT_FILE="$ROOT_DIR/out/graph.json"

echo "[1/3] 노트 검증 중..."
python3 "$SCRIPT_DIR/validate_vault.py" --vault "$ROOT_DIR/vault/papers"

echo "[2/3] 지식 그래프 생성 중..."
python3 "$SCRIPT_DIR/build_graph.py" --vault "$ROOT_DIR/vault/papers" --out "$OUT_FILE" --pretty

if [ ! -d "$PUBLIC_DIR" ]; then
  echo "오류: IBK_public 디렉터리를 찾을 수 없습니다: $PUBLIC_DIR" >&2
  echo "사용법: scripts/export_to_public.sh [IBK_public 경로]" >&2
  exit 1
fi

echo "[3/3] 공개 저장소로 복사 중..."
mkdir -p "$PUBLIC_DIR/data"
cp "$OUT_FILE" "$PUBLIC_DIR/data/graph.json"

echo "완료: $PUBLIC_DIR/data/graph.json 이 갱신되었습니다."
echo "이제 IBK_public 저장소에서 변경 사항을 확인하고 커밋하세요."
