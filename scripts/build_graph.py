#!/usr/bin/env python3
"""Build the public knowledge graph (graph.json) from the private paper vault.

MINIMAL CONTEXT principle (privacy-critical):
- Only YAML front matter metadata is read for export; note bodies are ignored.
- Exported node dicts are built from an explicit whitelist of fields.
  Authors, venue, body text, equations, quotes (원문 근거) and the relation
  "evidence" field are NEVER exported.
- Notes with permission "private" are never exported; every edge touching
  them is dropped; they only increment meta.counts.excluded_private.
- Edges are exported only when BOTH endpoints are exported.

Usage:
    python3 scripts/build_graph.py [--vault vault/papers] [--out out/graph.json]
                                   [--include-team] [--pretty]
"""

import argparse
import itertools
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
SOURCE_VAULT = "IBK_private"

VALID_PERMISSIONS = {"public", "team", "private"}

# Explicit (authored) relation weights by type.
EXPLICIT_EDGE_WEIGHTS = {
    "supports": 0.9,
    "extends": 0.8,
    "refutes": 0.7,
    "same-method": 0.6,
    "shares-data": 0.5,
}

EDGE_NOTE_MAX_LEN = 120
JACCARD_MIN = 0.15
OVERLAP_MAX_WEIGHT = 0.5

# Whitelist of node fields exported to the public graph. Anything not listed
# here (authors, venue, relation evidence, body text, ...) must never leave
# the private vault.
NODE_FIELDS = (
    "id", "title", "title_ko", "year", "permission", "status",
    "topics", "keywords", "methods", "source", "degree",
)


def warn(message):
    print(f"[build_graph] 경고: {message}", file=sys.stderr)


def _as_str(value):
    """Return a non-empty stripped string, or None."""
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _as_int(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _as_str_list(value):
    """Normalize to a sorted, de-duplicated list of non-empty strings."""
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    items = set()
    for item in value:
        text = _as_str(item)
        if text is not None:
            items.add(text)
    return sorted(items)


def parse_front_matter(path):
    """Parse the YAML front matter block of one note.

    Returns the front matter dict, or None (with a stderr warning) when the
    file has no front matter or the YAML does not parse. The note body below
    the closing '---' is never parsed or returned.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        warn(f"{path.name}: 파일을 읽을 수 없어 건너뜁니다 ({exc})")
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        warn(f"{path.name}: front matter가 없어 건너뜁니다")
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        warn(f"{path.name}: front matter를 닫는 '---' 구분선이 없어 건너뜁니다")
        return None
    try:
        front_matter = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        warn(f"{path.name}: YAML 파싱 실패로 건너뜁니다 ({exc})")
        return None
    if not isinstance(front_matter, dict):
        warn(f"{path.name}: front matter가 매핑 형식이 아니어서 건너뜁니다")
        return None
    return front_matter


def load_notes(vault_dir):
    """Parse every *.md note in the vault. Returns {note_id: record}.

    A record is {"id", "permission", "fm", "file"}. One bad note never
    aborts the build -- it is skipped with a warning.
    """
    notes = {}
    if not vault_dir.is_dir():
        warn(f"vault 디렉터리가 없습니다: {vault_dir}")
        return notes
    for path in sorted(vault_dir.glob("*.md")):
        try:
            front_matter = parse_front_matter(path)
            if front_matter is None:
                continue
            note_id = _as_str(front_matter.get("id"))
            if note_id is None:
                note_id = path.stem
                warn(f"{path.name}: id 필드가 없어 파일명 '{note_id}' 을 사용합니다")
            if note_id in notes:
                warn(f"{path.name}: 중복 id '{note_id}' - 먼저 읽은 노트를 유지합니다")
                continue
            permission = front_matter.get("permission", "private")
            if permission not in VALID_PERMISSIONS:
                warn(f"{path.name}: permission 값이 잘못되어 private으로 처리합니다: {permission!r}")
                permission = "private"
            notes[note_id] = {
                "id": note_id,
                "permission": permission,
                "fm": front_matter,
                "file": path.name,
            }
        except Exception as exc:  # never let one bad note break the build
            warn(f"{path.name}: 노트 처리 중 오류로 건너뜁니다 ({exc})")
    return notes


def make_node(record):
    """Build the exported node dict from an explicit field whitelist.

    NEVER dump the parsed front matter: authors, venue, evidence and any
    unknown fields must not reach the public graph.
    """
    front_matter = record["fm"]
    raw_source = front_matter.get("source")
    if not isinstance(raw_source, dict):
        raw_source = {}
    node = {
        "id": record["id"],
        "title": _as_str(front_matter.get("title")) or record["id"],
        "title_ko": _as_str(front_matter.get("title_ko")),
        "year": _as_int(front_matter.get("year")),
        "permission": record["permission"],
        "status": _as_str(front_matter.get("status")) or "read",
        "topics": _as_str_list(front_matter.get("topics")),
        "keywords": _as_str_list(front_matter.get("keywords")),
        "methods": _as_str_list(front_matter.get("methods")),
        "source": {
            "drive_path": _as_str(raw_source.get("drive_path")),
            "drive_url": _as_str(raw_source.get("drive_url")),
            "doi": _as_str(front_matter.get("doi")),
        },
        "degree": 0,
    }
    # Safety net: the exported shape is exactly the whitelist, nothing more.
    assert set(node) == set(NODE_FIELDS)
    return node


def collect_explicit_edges(notes, exported_ids):
    """Collect authored relation edges between exported notes.

    Returns (edges, linked_pairs) where linked_pairs is the set of unordered
    id pairs that carry at least one explicit edge. Only the "note" field of
    a relation is exported (truncated); "evidence" is never read into an edge.
    """
    edges = []
    seen_keys = set()      # (frozenset({a, b}), type) for de-duplication
    linked_pairs = set()   # frozenset({a, b})
    for note_id in sorted(exported_ids):
        relations = notes[note_id]["fm"].get("relations")
        if relations is None:
            continue
        if not isinstance(relations, list):
            warn(f"{note_id}: relations 필드가 리스트가 아니어서 무시합니다")
            continue
        for relation in relations:
            if not isinstance(relation, dict):
                warn(f"{note_id}: 관계 항목이 매핑 형식이 아니어서 제외합니다: {relation!r}")
                continue
            rel_type = relation.get("type")
            target = _as_str(relation.get("target"))
            if rel_type not in EXPLICIT_EDGE_WEIGHTS:
                warn(f"{note_id}: 알 수 없는 관계 type {rel_type!r} - 제외합니다")
                continue
            if target is None:
                warn(f"{note_id}: 관계에 target이 없어 제외합니다 (type={rel_type})")
                continue
            if target == note_id:
                warn(f"{note_id}: 자기 자신을 가리키는 관계를 제외합니다")
                continue
            if target not in notes:
                warn(f"{note_id}: 존재하지 않는 대상 '{target}' 에 대한 관계를 제외합니다")
                continue
            if target not in exported_ids:
                warn(f"{note_id}: 내보내지 않는 노트 '{target}' 에 대한 관계를 제외합니다")
                continue
            key = (frozenset((note_id, target)), rel_type)
            if key in seen_keys:
                warn(f"{note_id}: 중복 관계 ({rel_type} -> {target}) - 하나만 유지합니다")
                continue
            seen_keys.add(key)
            linked_pairs.add(frozenset((note_id, target)))
            note_text = _as_str(relation.get("note"))
            if note_text is not None:
                note_text = note_text[:EDGE_NOTE_MAX_LEN]
            edges.append({
                "source": note_id,
                "target": target,
                "type": rel_type,
                "weight": EXPLICIT_EDGE_WEIGHTS[rel_type],
                "explicit": True,
                "note": note_text,
            })
    return edges, linked_pairs


def collect_overlap_edges(nodes, linked_pairs):
    """Compute implicit keyword-overlap edges.

    For each unordered pair of exported nodes with NO explicit edge, the
    Jaccard similarity of set(topics + keywords) is computed; pairs with
    j >= JACCARD_MIN get a keyword-overlap edge, weight capped at 0.5.
    """
    tag_sets = {
        node_id: set(node["topics"]) | set(node["keywords"])
        for node_id, node in nodes.items()
    }
    edges = []
    for id_a, id_b in itertools.combinations(sorted(nodes), 2):
        if frozenset((id_a, id_b)) in linked_pairs:
            continue
        tags_a, tags_b = tag_sets[id_a], tag_sets[id_b]
        if not tags_a or not tags_b:
            continue
        union = tags_a | tags_b
        jaccard = len(tags_a & tags_b) / len(union)
        if jaccard >= JACCARD_MIN:
            edges.append({
                "source": id_a,
                "target": id_b,
                "type": "keyword-overlap",
                "weight": round(min(OVERLAP_MAX_WEIGHT, jaccard), 3),
                "explicit": False,
                "note": None,
            })
    return edges


def build_graph(vault_dir, include_team=False):
    """Build the full graph dict per the public schema. Deterministic."""
    notes = load_notes(Path(vault_dir))
    allowed = {"public", "team"} if include_team else {"public"}
    exported_ids = {nid for nid, rec in notes.items() if rec["permission"] in allowed}
    excluded_private = sum(1 for rec in notes.values() if rec["permission"] == "private")

    nodes = {nid: make_node(notes[nid]) for nid in exported_ids}
    explicit_edges, linked_pairs = collect_explicit_edges(notes, exported_ids)
    overlap_edges = collect_overlap_edges(nodes, linked_pairs)
    edges = sorted(
        explicit_edges + overlap_edges,
        key=lambda e: (e["source"], e["target"], e["type"]),
    )

    degree = Counter()
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1
    for node_id, node in nodes.items():
        node["degree"] = degree.get(node_id, 0)

    node_list = [nodes[nid] for nid in sorted(nodes)]
    topics = sorted({t for node in node_list for t in node["topics"]})
    keywords = sorted({k for node in node_list for k in node["keywords"]})
    edge_types = dict(sorted(Counter(e["type"] for e in edges).items()))

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).date().isoformat(),
        "source_vault": SOURCE_VAULT,
        "nodes": node_list,
        "edges": edges,
        "meta": {
            "topics": topics,
            "keywords": keywords,
            "counts": {
                "nodes": len(node_list),
                "edges": len(edges),
                "excluded_private": excluded_private,
            },
            "edge_types": edge_types,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="비공개 vault에서 최소 컨텍스트 지식 그래프(graph.json)를 추출합니다.",
    )
    parser.add_argument("--vault", default="vault/papers",
                        help="노트 디렉터리 (기본값: vault/papers)")
    parser.add_argument("--out", default="out/graph.json",
                        help="출력 파일 경로 (기본값: out/graph.json)")
    parser.add_argument("--include-team", action="store_true",
                        help="permission: team 노트도 포함합니다 (팀 내부 배포용 — "
                             "세계 공개 저장소에는 사용하지 마세요). 기본값은 public 전용.")
    parser.add_argument("--pretty", action="store_true",
                        help="사람이 읽기 좋은 들여쓰기 JSON으로 출력합니다")
    args = parser.parse_args(argv)

    graph = build_graph(Path(args.vault), include_team=args.include_team)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        if args.pretty:
            json.dump(graph, handle, ensure_ascii=False, indent=2, sort_keys=True)
        else:
            json.dump(graph, handle, ensure_ascii=False,
                      separators=(",", ":"), sort_keys=True)
        handle.write("\n")

    counts = graph["meta"]["counts"]
    print(
        f"그래프 생성 완료: 노드 {counts['nodes']}개, 엣지 {counts['edges']}개, "
        f"제외된 비공개 노트 {counts['excluded_private']}개 -> {out_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
