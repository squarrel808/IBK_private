#!/usr/bin/env python3
"""Unit tests for build_graph.py (stdlib unittest, self-contained fixtures).

Fixture graph written to a tempdir:

  n-alpha   (public)  --supports-->   n-beta    (note > 120 chars, evidence marker)
  n-alpha   (public)  --extends-->    n-gamma   (duplicated in reverse by n-gamma)
  n-alpha   (public)  --refutes-->    n-priv    (private target: must be dropped)
  n-alpha   (public)  --same-method-> n-ghost   (nonexistent target: must be dropped)
  n-alpha   (public)  --shares-data-> n-delta
  n-beta    (team)    --refutes-->    n-gamma
  n-beta    (team)    --same-method-> n-delta
  n-priv    (private) --supports-->   n-alpha   (private source: must be dropped)

  Implicit keyword-overlap (pairs without explicit edges):
    n-beta  <-> n-epsilon  jaccard 1/6 = 0.167
    n-delta <-> n-epsilon  jaccard 3/5 = 0.6 -> weight capped at 0.5
"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import build_graph  # noqa: E402

# Unique marker strings that must NEVER appear in any serialized output.
BODY_MARKER = "BODY-SECRET-MARKER-XYZZY-7f3a"
EVIDENCE_MARKER = "EVIDENCE-SECRET-MARKER-PLUGH-9c1d"
AUTHOR_MARKER = "Zzauthorsecretsurname"
VENUE_MARKER = "Zzvenuesecretjournal"
PRIV_TITLE_MARKER = "Zzprivatetitlesecret"
TAIL_MARKER = "ZZ-TRUNCATED-TAIL-MARKER"

LONG_NOTE = "n" * 110 + TAIL_MARKER  # 134 chars, must be truncated to 120

NODE_FIELD_SET = {
    "id", "title", "title_ko", "year", "permission", "status",
    "topics", "keywords", "methods", "source", "degree",
}


def note_text(front_matter, body):
    dumped = yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False)
    return f"---\n{dumped}---\n\n{body}\n"


def write_note(vault, front_matter, body="placeholder body"):
    path = vault / f"{front_matter['id']}.md"
    path.write_text(note_text(front_matter, body), encoding="utf-8")


def write_fixtures(vault):
    write_note(vault, {
        "id": "n-alpha",
        "title": "Alpha Paper on Factor Models",
        "title_ko": "알파 논문",
        "authors": [f"{AUTHOR_MARKER}, A.", "Kim, B."],
        "year": 2020,
        "venue": VENUE_MARKER,
        "doi": "10.1000/alpha",
        "source": {
            "drive_path": "IBK/papers/alpha.pdf",
            "drive_url": "https://drive.google.com/alpha",
        },
        "permission": "public",
        "status": "read",
        "topics": ["t-one"],
        "keywords": ["k-shared", "k-alpha"],
        "methods": ["m-ols"],
        "relations": [
            {"type": "supports", "target": "n-beta",
             "note": LONG_NOTE, "evidence": f"{EVIDENCE_MARKER} p.3"},
            {"type": "extends", "target": "n-gamma"},
            {"type": "refutes", "target": "n-priv",
             "note": "비공개 노트로의 관계", "evidence": "p.9"},
            {"type": "same-method", "target": "n-ghost"},
            {"type": "shares-data", "target": "n-delta"},
        ],
        "created": "2026-08-31",
        "updated": "2026-08-31",
    }, body=f"# Alpha\n## 한 줄 요약\n{BODY_MARKER}\n## 핵심 수식\n$$y = X\\beta$$\n")

    write_note(vault, {
        "id": "n-beta",
        "title": "Beta Paper",
        "authors": ["Lee, C."],
        "year": 2021,
        "permission": "team",
        "status": "skimmed",
        "topics": ["t-one"],
        "keywords": ["k-shared", "k-b"],
        "relations": [
            {"type": "refutes", "target": "n-gamma"},
            {"type": "same-method", "target": "n-delta"},
        ],
    })

    write_note(vault, {
        "id": "n-gamma",
        "title": "Gamma Paper",
        "authors": ["Park, D."],
        "year": 2019,
        "permission": "public",
        "status": "read",
        "topics": ["t-one"],
        "keywords": ["k-shared", "k-g"],
        "relations": [
            # Reverse duplicate of n-alpha --extends--> n-gamma (same unordered
            # pair + same type): exactly one must survive.
            {"type": "extends", "target": "n-alpha", "note": "중복 엣지 테스트"},
        ],
    })

    write_note(vault, {
        "id": "n-delta",
        "title": "Delta Paper",
        "authors": ["Choi, E."],
        "year": 2022,
        "permission": "public",
        "status": "read",
        "topics": ["t-x"],
        "keywords": ["k-a", "k-b", "k-c"],
    })

    write_note(vault, {
        "id": "n-epsilon",
        "title": "Epsilon Paper",
        "authors": ["Jung, F."],
        "year": 2023,
        "permission": "public",
        "status": "to-verify",
        "topics": ["t-x"],
        "keywords": ["k-a", "k-b", "k-d"],
    })

    write_note(vault, {
        "id": "n-priv",
        "title": f"{PRIV_TITLE_MARKER} internal memo",
        "authors": ["Private, P."],
        "year": 2026,
        "permission": "private",
        "status": "read",
        # High overlap with n-alpha on purpose: still no edge may touch it.
        "topics": ["t-one"],
        "keywords": ["k-shared", "k-alpha"],
        "relations": [
            {"type": "supports", "target": "n-alpha",
             "evidence": "private evidence text"},
        ],
    })

    # Robustness fixtures: must be skipped with a warning, never crash.
    (vault / "no-front-matter.md").write_text(
        "just a plain markdown file without front matter\n", encoding="utf-8")
    (vault / "bad-yaml.md").write_text(
        "---\nid: [unclosed\n---\nbody\n", encoding="utf-8")


def run_build(vault, include_team=False):
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        graph = build_graph.build_graph(vault, include_team=include_team)
    return graph, stderr.getvalue()


class BuildGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp_path = Path(cls._tmp.name)
        cls.vault = cls.tmp_path / "vault" / "papers"
        cls.vault.mkdir(parents=True)
        write_fixtures(cls.vault)
        cls.graph, cls.stderr = run_build(cls.vault, include_team=True)
        cls.graph_public, cls.stderr_public = run_build(cls.vault, include_team=False)
        cls.serialized = json.dumps(cls.graph, ensure_ascii=False, sort_keys=True)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    # ---- helpers ----------------------------------------------------------

    def node_ids(self, graph=None):
        return [node["id"] for node in (graph or self.graph)["nodes"]]

    def find_edge(self, source, target, edge_type, graph=None):
        for edge in (graph or self.graph)["edges"]:
            if (edge["source"], edge["target"], edge["type"]) == (source, target, edge_type):
                return edge
        return None

    # ---- (a) private notes fully excluded ---------------------------------

    def test_private_note_excluded(self):
        self.assertNotIn("n-priv", self.node_ids())
        for edge in self.graph["edges"]:
            self.assertNotEqual(edge["source"], "n-priv")
            self.assertNotEqual(edge["target"], "n-priv")
        self.assertEqual(self.graph["meta"]["counts"]["excluded_private"], 1)
        # The private note's id and title must not appear anywhere at all.
        self.assertNotIn("n-priv", self.serialized)
        self.assertNotIn(PRIV_TITLE_MARKER, self.serialized)

    # ---- (b) body / evidence never leak -----------------------------------

    def test_body_and_evidence_markers_never_serialized(self):
        self.assertNotIn(BODY_MARKER, self.serialized)
        self.assertNotIn(EVIDENCE_MARKER, self.serialized)

    def test_cli_output_file_has_no_private_content(self):
        out_file = self.tmp_path / "out" / "graph.json"
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = build_graph.main([
                "--vault", str(self.vault), "--out", str(out_file), "--pretty",
            ])
        self.assertEqual(rc, 0)
        text = out_file.read_text(encoding="utf-8")
        parsed = json.loads(text)  # valid JSON
        self.assertEqual(parsed["schema_version"], 1)
        for marker in (BODY_MARKER, EVIDENCE_MARKER, AUTHOR_MARKER,
                       VENUE_MARKER, PRIV_TITLE_MARKER, TAIL_MARKER, "n-priv"):
            self.assertNotIn(marker, text)

    # ---- (c) authors / venue never exported --------------------------------

    def test_authors_and_venue_not_exported(self):
        self.assertNotIn(AUTHOR_MARKER, self.serialized)
        self.assertNotIn(VENUE_MARKER, self.serialized)
        for node in self.graph["nodes"]:
            self.assertEqual(set(node), NODE_FIELD_SET)
            self.assertEqual(set(node["source"]), {"drive_path", "drive_url", "doi"})

    # ---- (d) explicit edge weights by type ---------------------------------

    def test_explicit_edge_weights(self):
        explicit = {
            (edge["source"], edge["target"], edge["type"]): edge["weight"]
            for edge in self.graph["edges"] if edge["explicit"]
        }
        self.assertEqual(explicit, {
            ("n-alpha", "n-beta", "supports"): 0.9,
            ("n-alpha", "n-gamma", "extends"): 0.8,
            ("n-alpha", "n-delta", "shares-data"): 0.5,
            ("n-beta", "n-gamma", "refutes"): 0.7,
            ("n-beta", "n-delta", "same-method"): 0.6,
        })

    def test_duplicate_explicit_edge_kept_once(self):
        extends_pairs = [
            frozenset((edge["source"], edge["target"]))
            for edge in self.graph["edges"] if edge["type"] == "extends"
        ]
        self.assertEqual(
            extends_pairs.count(frozenset(("n-alpha", "n-gamma"))), 1)

    # ---- (e) keyword-overlap edges -----------------------------------------

    def test_keyword_overlap_edges(self):
        overlap = {
            (edge["source"], edge["target"]): edge
            for edge in self.graph["edges"] if edge["type"] == "keyword-overlap"
        }
        self.assertEqual(set(overlap), {
            ("n-beta", "n-epsilon"),
            ("n-delta", "n-epsilon"),
        })
        # jaccard 1/6 -> round(0.1666..., 3) == 0.167
        self.assertEqual(overlap[("n-beta", "n-epsilon")]["weight"], 0.167)
        # jaccard 0.6 -> capped at 0.5
        self.assertEqual(overlap[("n-delta", "n-epsilon")]["weight"], 0.5)
        for edge in overlap.values():
            self.assertFalse(edge["explicit"])
            self.assertIsNone(edge["note"])
            self.assertLessEqual(edge["weight"], 0.5)
        # n-alpha and n-gamma have jaccard 0.5 >= 0.15 but an explicit edge,
        # so no keyword-overlap edge may exist between them.
        self.assertIsNone(self.find_edge("n-alpha", "n-gamma", "keyword-overlap"))

    # ---- (f) default export drops team notes (--include-team opts in) ------

    def test_default_export_drops_team_nodes(self):
        self.assertEqual(self.node_ids(self.graph_public),
                         ["n-alpha", "n-delta", "n-epsilon", "n-gamma"])
        for node in self.graph_public["nodes"]:
            self.assertEqual(node["permission"], "public")
        edge_keys = {
            (edge["source"], edge["target"], edge["type"])
            for edge in self.graph_public["edges"]
        }
        self.assertEqual(edge_keys, {
            ("n-alpha", "n-gamma", "extends"),
            ("n-alpha", "n-delta", "shares-data"),
            ("n-delta", "n-epsilon", "keyword-overlap"),
        })
        self.assertEqual(self.graph_public["meta"]["counts"]["excluded_private"], 1)

    # ---- (g) nonexistent relation target dropped without crash -------------

    def test_nonexistent_target_dropped(self):
        for edge in self.graph["edges"]:
            self.assertNotIn("n-ghost", (edge["source"], edge["target"]))
        self.assertNotIn("n-ghost", self.serialized)
        self.assertIn("n-ghost", self.stderr)  # warning was emitted

    # ---- (h) edge note truncated to 120 chars ------------------------------

    def test_edge_note_truncated(self):
        edge = self.find_edge("n-alpha", "n-beta", "supports")
        self.assertIsNotNone(edge)
        self.assertEqual(len(edge["note"]), 120)
        self.assertEqual(edge["note"], LONG_NOTE[:120])
        self.assertNotIn(TAIL_MARKER, self.serialized)

    # ---- (i) degree --------------------------------------------------------

    def test_degree_counts(self):
        degrees = {node["id"]: node["degree"] for node in self.graph["nodes"]}
        self.assertEqual(degrees, {
            "n-alpha": 3,
            "n-beta": 4,
            "n-gamma": 2,
            "n-delta": 3,
            "n-epsilon": 2,
        })

    # ---- schema / meta / determinism ---------------------------------------

    def test_meta_counts_and_edge_types(self):
        meta = self.graph["meta"]
        self.assertEqual(meta["counts"],
                         {"nodes": 5, "edges": 7, "excluded_private": 1})
        self.assertEqual(meta["edge_types"], {
            "extends": 1,
            "keyword-overlap": 2,
            "refutes": 1,
            "same-method": 1,
            "shares-data": 1,
            "supports": 1,
        })
        self.assertEqual(meta["topics"], ["t-one", "t-x"])
        self.assertEqual(meta["keywords"],
                         ["k-a", "k-alpha", "k-b", "k-c", "k-d", "k-g", "k-shared"])

    def test_top_level_schema(self):
        self.assertEqual(
            set(self.graph),
            {"schema_version", "generated_at", "source_vault", "nodes", "edges", "meta"},
        )
        self.assertEqual(self.graph["schema_version"], 1)
        self.assertEqual(self.graph["source_vault"], "IBK_private")
        # Broken fixture files were skipped with warnings, not crashes.
        self.assertIn("no-front-matter.md", self.stderr)
        self.assertIn("bad-yaml.md", self.stderr)

    def test_deterministic_output(self):
        rebuilt, _ = run_build(self.vault, include_team=True)
        self.assertEqual(
            json.dumps(rebuilt, ensure_ascii=False, sort_keys=True),
            self.serialized,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
