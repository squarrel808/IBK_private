#!/usr/bin/env python3
"""Lint every note in the vault against the front matter schema.

Checks (all error messages in Korean, with file:line context):
- front matter exists and parses as a YAML mapping
- required fields present and correctly typed
  (id, title, authors, year, permission, status, topics, keywords, created, updated)
- permission / status / relation "type" values are within the allowed sets
- id matches the filename stem and is kebab-case
- topics / keywords / methods entries are kebab-case
- relation targets exist somewhere in the vault
- relation "note" is at most 120 characters
- duplicate ids across files
- the 9 standard body sections are present and in the standard order
- every relation target appears as a [[wikilink]] in the note body

Exit code 1 when any error is found.
Final summary line: "N개 노트 검사, M개 오류".
"""

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

import yaml

KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_PERMISSIONS = ("public", "team", "private")
VALID_STATUSES = ("read", "skimmed", "to-verify")
VALID_RELATION_TYPES = ("supports", "refutes", "extends", "same-method", "shares-data")
EDGE_NOTE_MAX_LEN = 120
REQUIRED_FIELDS = ("id", "title", "authors", "year", "permission", "status",
                   "topics", "keywords", "created", "updated")
REQUIRED_SECTIONS = ("한 줄 요약", "핵심 주장", "연구 방법", "주요 결과", "핵심 수식",
                     "한계와 공백", "참고문헌", "원문 근거", "연결 노트")


def field_line(block_lines, field):
    """Best-effort 1-based file line of a top-level front matter field."""
    pattern = re.compile(rf"^\s*{re.escape(field)}\s*:")
    for index, line in enumerate(block_lines):
        if pattern.match(line):
            return index + 2  # +1 for the opening '---', +1 for 1-based lines
    return 1


def parse_note(path, errors):
    """Parse one note file. Returns (front_matter | None, block_lines, body_lines)."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{path}:1: 파일을 읽을 수 없습니다 ({exc})")
        return None, [], []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(
            f"{path}:1: front matter(YAML 머리말)가 없습니다 - 파일이 '---' 로 시작해야 합니다"
        )
        return None, [], []
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        errors.append(f"{path}:1: front matter를 닫는 '---' 구분선이 없습니다")
        return None, [], []
    block = lines[1:end]
    body = lines[end + 1:]
    try:
        front_matter = yaml.safe_load("\n".join(block))
    except yaml.YAMLError as exc:
        line = 2
        mark = getattr(exc, "problem_mark", None)
        if mark is not None:
            line = mark.line + 2
        errors.append(f"{path}:{line}: YAML 파싱 오류: {exc}")
        return None, block, body
    if not isinstance(front_matter, dict):
        errors.append(f"{path}:2: front matter가 'key: value' 매핑 형식이 아닙니다")
        return None, block, body
    return front_matter, block, body


def validate_note(path, front_matter, block, errors):
    """Field-level checks for one parsed note."""

    def err(field, message):
        errors.append(f"{path}:{field_line(block, field)}: {message}")

    for field in REQUIRED_FIELDS:
        if field not in front_matter or front_matter[field] is None:
            errors.append(f"{path}:1: 필수 필드 '{field}' 이(가) 없습니다")

    note_id = front_matter.get("id")
    if note_id is not None:
        if not isinstance(note_id, str):
            err("id", "'id' 필드는 문자열이어야 합니다")
        else:
            if note_id != path.stem:
                err("id", f"id '{note_id}' 이(가) 파일명 '{path.stem}' 과 일치하지 않습니다")
            if not KEBAB_RE.match(note_id):
                err("id", f"id '{note_id}' 은(는) kebab-case여야 합니다 "
                          "(예: gu2020-ml-asset-pricing)")

    title = front_matter.get("title")
    if title is not None and not isinstance(title, str):
        err("title", "'title' 필드는 문자열이어야 합니다")

    for field in ("title_ko", "venue", "doi"):
        value = front_matter.get(field)
        if value is not None and not isinstance(value, str):
            err(field, f"'{field}' 필드는 문자열이어야 합니다")

    authors = front_matter.get("authors")
    if authors is not None:
        if not isinstance(authors, list) or not authors:
            err("authors", "'authors' 필드는 비어 있지 않은 리스트여야 합니다")
        elif not all(isinstance(a, str) and a.strip() for a in authors):
            err("authors", "'authors' 리스트의 모든 항목은 문자열이어야 합니다")

    year = front_matter.get("year")
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
        err("year", f"'year' 필드는 정수여야 합니다 (현재 값: {year!r})")

    permission = front_matter.get("permission")
    if permission is not None and permission not in VALID_PERMISSIONS:
        err("permission", f"permission 값이 잘못되었습니다: {permission!r} "
                          "(허용값: public, team, private)")

    status = front_matter.get("status")
    if status is not None and status not in VALID_STATUSES:
        err("status", f"status 값이 잘못되었습니다: {status!r} "
                      "(허용값: read, skimmed, to-verify)")

    for field, required in (("topics", True), ("keywords", True), ("methods", False)):
        value = front_matter.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            err(field, f"'{field}' 필드는 리스트여야 합니다")
            continue
        if required and not value:
            err(field, f"'{field}' 리스트가 비어 있습니다 - 최소 1개 항목이 필요합니다")
        for item in value:
            if not isinstance(item, str) or not KEBAB_RE.match(item):
                err(field, f"{field} 항목 {item!r} 은(는) kebab-case가 아닙니다 "
                           "(예: asset-pricing)")

    source = front_matter.get("source")
    if source is not None:
        if not isinstance(source, dict):
            err("source", "'source' 필드는 매핑(drive_path, drive_url)이어야 합니다")
        else:
            for key in ("drive_path", "drive_url"):
                value = source.get(key)
                if value is not None and not isinstance(value, str):
                    err("source", f"source.{key} 은(는) 문자열이어야 합니다")

    for field in ("created", "updated"):
        value = front_matter.get(field)
        if value is not None and not isinstance(value, (str, _dt.date)):
            err(field, f"'{field}' 필드는 날짜(YYYY-MM-DD)여야 합니다")


def validate_relations(path, front_matter, block, all_ids, errors):
    """Relation-level checks; targets must exist somewhere in the vault."""
    relations = front_matter.get("relations")
    if relations is None:
        return
    base_line = field_line(block, "relations")
    if not isinstance(relations, list):
        errors.append(f"{path}:{base_line}: 'relations' 필드는 리스트여야 합니다")
        return
    for index, relation in enumerate(relations):
        prefix = f"{path}:{base_line}: relations[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{prefix}: 관계 항목은 매핑(type/target/...)이어야 합니다")
            continue
        rel_type = relation.get("type")
        if rel_type not in VALID_RELATION_TYPES:
            errors.append(
                f"{prefix}: type 값이 잘못되었습니다: {rel_type!r} "
                f"(허용값: {', '.join(VALID_RELATION_TYPES)})"
            )
        target = relation.get("target")
        if not isinstance(target, str) or not target.strip():
            errors.append(f"{prefix}: target 이 없거나 문자열이 아닙니다")
        elif target == front_matter.get("id"):
            errors.append(f"{prefix}: target 이 자기 자신을 가리킵니다")
        elif target not in all_ids:
            errors.append(f"{prefix}: target '{target}' 노트가 vault에 존재하지 않습니다")
        note = relation.get("note")
        if note is not None:
            if not isinstance(note, str):
                errors.append(f"{prefix}: note 는 문자열이어야 합니다")
            elif len(note) > EDGE_NOTE_MAX_LEN:
                errors.append(
                    f"{prefix}: note 가 {EDGE_NOTE_MAX_LEN}자를 초과합니다 (현재 {len(note)}자)"
                )
        evidence = relation.get("evidence")
        if evidence is not None and not isinstance(evidence, str):
            errors.append(f"{prefix}: evidence 는 문자열이어야 합니다")


def validate_body(path, front_matter, body, fm_offset, errors):
    """Body checks: standard section presence/order + relation wikilinks."""
    headings = []
    for index, line in enumerate(body):
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            headings.append((match.group(1), fm_offset + index + 1))

    heading_titles = [title for title, _ in headings]
    positions = []
    for section in REQUIRED_SECTIONS:
        if section in heading_titles:
            positions.append((section, heading_titles.index(section)))
        else:
            errors.append(f"{path}:1: 본문에 '## {section}' 섹션이 없습니다")
    for (prev_name, prev_pos), (name, pos) in zip(positions, positions[1:]):
        if pos < prev_pos:
            line = headings[pos][1]
            errors.append(
                f"{path}:{line}: 본문 섹션 순서가 표준과 다릅니다 - "
                f"'## {name}' 이 '## {prev_name}' 보다 앞에 있습니다"
            )

    relations = front_matter.get("relations")
    if isinstance(relations, list):
        body_text = "\n".join(body)
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict):
                continue
            target = relation.get("target")
            if isinstance(target, str) and target.strip():
                if f"[[{target}" not in body_text:
                    errors.append(
                        f"{path}:1: relations[{index}] 의 target '{target}' 이(가) "
                        f"본문 '연결 노트' 섹션에 [[{target}]] wikilink로 없습니다"
                    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="vault 노트 front matter 검증 도구")
    parser.add_argument("--vault", default="vault/papers",
                        help="노트 디렉터리 (기본값: vault/papers)")
    args = parser.parse_args(argv)

    vault = Path(args.vault)
    if not vault.is_dir():
        print(f"오류: vault 디렉터리를 찾을 수 없습니다: {vault}", file=sys.stderr)
        print("0개 노트 검사, 1개 오류")
        return 1

    files = sorted(vault.glob("*.md"))
    errors = []
    parsed = []
    ids = {}

    # First pass: parse everything and collect the vault-wide id set.
    for path in files:
        front_matter, block, body = parse_note(path, errors)
        parsed.append((path, front_matter, block, body))
        if front_matter is None:
            continue
        note_id = front_matter.get("id")
        if isinstance(note_id, str):
            if note_id in ids:
                line = field_line(block, "id")
                errors.append(
                    f"{path}:{line}: 중복된 id '{note_id}' (먼저 사용된 파일: {ids[note_id]})"
                )
            else:
                ids[note_id] = path.name

    # Second pass: field checks + relation target existence.
    all_ids = set(ids)
    for path, front_matter, block, body in parsed:
        if front_matter is None:
            continue
        validate_note(path, front_matter, block, errors)
        validate_relations(path, front_matter, block, all_ids, errors)
        # +2: opening/closing '---' lines before the body starts.
        validate_body(path, front_matter, body, len(block) + 2, errors)

    for message in errors:
        print(message, file=sys.stderr)
    if not errors:
        print("문제가 발견되지 않았습니다.")
    print(f"{len(files)}개 노트 검사, {len(errors)}개 오류")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
