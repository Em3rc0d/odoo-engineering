#!/usr/bin/env python3
"""Local structural validator for Odoo Engineering; stdlib only, no network."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

def fail(message: str): ERRORS.append(message)

def load(path: str):
    p = ROOT / path
    if not p.is_file(): fail(f"Missing {path}"); return {}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: fail(f"Invalid JSON {path}: {exc}"); return {}

def check_common(entry, category):
    if not isinstance(entry, dict): fail(f"Invalid {category} entry: {entry!r}"); return
    if not entry.get('id'): fail(f"{category} missing ID")

catalog = load('research/sources/catalog.json')
findings = load('findings/index.json')
patterns = load('patterns/index.json')
sources = catalog.get('sources', [])
fnds = findings.get('entries', [])
pats = patterns.get('entries', [])
source_ids = {s.get('id') for s in sources if isinstance(s, dict)}
finding_ids = {f.get('id') for f in fnds if isinstance(f, dict)}
pattern_ids = {p.get('id') for p in pats if isinstance(p, dict)}
for name, records, ids in [('sources',sources,source_ids),('findings',fnds,finding_ids),('patterns',pats,pattern_ids)]:
    if len(ids)!=len(records): fail(f"Duplicate/missing {name} IDs")
for s in sources:
    check_common(s,'source')
    if not re.fullmatch(r'[a-f0-9]{40}',s.get('ref','')): fail(f"Source {s.get('id')} must pin SHA40")
    if not s.get('url','').startswith('https://github.com/'): fail(f"Invalid source URL: {s.get('id')}")
    if s.get('runtime') == 'RUNTIME_VALIDATED' and not (s.get('evidence') and (ROOT/s['evidence']).is_file()): fail(f"Missing runtime evidence: {s.get('id')}")
for f in fnds:
    check_common(f,'finding')
    if f.get('source') not in source_ids: fail(f"{f.get('id')}: missing source {f.get('source')}")
    if not re.fullmatch(r'FND-\d{3}',f.get('id','')): fail(f"Finding ID format {f.get('id')}")
    if not f.get('path') or not f.get('url','').startswith('https://github.com/'): fail(f"Finding lacks source link {f.get('id')}")
    if not f.get('lines') or len(f['lines'])!=2: fail(f"Finding missing lines {f.get('id')}")
    if f.get('confidence') not in {'STATIC_OBSERVATION','OFFICIAL_REFERENCE','INFERRED','RUNTIME_VALIDATED'}: fail(f"Bad status {f.get('id')}")
    if f.get('confidence') == 'RUNTIME_VALIDATED' and not (f.get('evidence') and (ROOT/f['evidence']).is_file()): fail(f"No test artifact for RUNTIME_VALIDATED: {f.get('id')}")
    if not (ROOT / f.get('document','')).is_file(): fail(f"No finding document: {f.get('id')}")
for p in pats:
    check_common(p,'pattern')
    if not re.fullmatch(r'PAT-\d{3}',p.get('id','')): fail(f"Pattern ID format {p.get('id')}")
    if not p.get('findings') or any(x not in finding_ids for x in p.get('findings',[])): fail(f"Broken finding reference: {p.get('id')}")
    if p.get('status') not in {'DOCUMENTED_NOT_RUNTIME_VALIDATED','RUNTIME_VALIDATED','REJECTED'}: fail(f"Invalid pattern status: {p.get('id')}")
    if p.get('status') == 'RUNTIME_VALIDATED' and not (p.get('evidence') and (ROOT/p['evidence']).is_file()): fail(f"Missing runtime evidence: {p.get('id')}")
    if not (ROOT / p.get('document','')).is_file(): fail(f"No pattern document: {p.get('id')}")
required=['README.md','AGENTS.md','CONTRIBUTING.md','research/MK0/README.md','research/MK1/README.md','docs/quality-gates.md','docs/official-references.md','research/sources/LICENSE_REVIEW.md']
for path in required:
    if not (ROOT/path).is_file(): fail(f"Required document missing: {path}")
if len(sources)!=5: fail(f"Expected first audited scope of 5 sources; got {len(sources)}")
print(f"Odoo Engineering | sources={len(sources)} findings={len(fnds)} patterns={len(pats)}")
if ERRORS:
    for err in ERRORS: print('FAIL:',err,file=sys.stderr)
    sys.exit(1)
print('PASS — documental integrity only; DOES NOT execute Odoo tests or verify third-party licenses.')
