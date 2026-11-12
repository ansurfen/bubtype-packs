#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install pack JSON files into BubType app_data (offline / no GitHub).

Default target (Windows Pro):
  %APPDATA%/app.bubtype.overlay/wordbooks

Usage:
  python scripts/install_local_to_appdata.py
  python scripts/install_local_to_appdata.py zh-hsk-1-3 ja-jlpt-n5n4
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_IDS = [
    "zh-hsk-1-3",
    "ja-jlpt-n5n4",
    "ko-core-beginner",
    "zh-daily-a1",
    "ja-daily-a1",
    "ko-daily-a1-zh",
    "es-daily-a1-zh",
    "fr-daily-a1-zh",
    "fr-core-a1-zh",
]


def app_wordbooks_root() -> Path:
    override = os.environ.get("BUBTYPE_WORDBOOKS")
    if override:
        return Path(override)
    roaming = os.environ.get("APPDATA") or ""
    return Path(roaming) / "app.bubtype.overlay" / "wordbooks"


def pack_file(pack_id: str) -> Path:
    direct = ROOT / f"{pack_id}-v1.json"
    if direct.exists():
        return direct
    # allow already-normalized id.json
    alt = ROOT / f"{pack_id}.json"
    if alt.exists():
        return alt
    raise FileNotFoundError(pack_id)


def install_one(wb_root: Path, pack_id: str) -> dict:
    packs_dir = wb_root / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)
    raw = json.loads(pack_file(pack_id).read_text(encoding="utf-8"))
    manifest = raw.get("manifest") or {}
    items = raw.get("items") or []
    lemmas = raw.get("lemmas") or []
    entries = raw.get("entries") or []

    pid = (manifest.get("id") or pack_id).strip()
    title = (manifest.get("title") or pid).strip()
    version = (manifest.get("version") or "1.0.0").strip()
    lang = (manifest.get("lang") or "en").strip()
    gloss_lang = manifest.get("glossLang")
    lemma_count = len(items) if items else len(lemmas)

    # Normalize pack stored on disk (keep spell/hint).
    norm_items = []
    for it in items:
        text = (it.get("text") or "").strip()
        if not text:
            continue
        row = {"text": text, "kind": it.get("kind") or "phrase"}
        hint = (it.get("hint") or "").strip()
        spell = (it.get("spell") or "").strip()
        if hint:
            row["hint"] = hint
        if spell:
            row["spell"] = spell
        norm_items.append(row)

    pack = {
        "manifest": {
            "id": pid,
            "title": title,
            "version": version,
            "lang": lang,
            "glossLang": gloss_lang,
            "source": "local",
            "lemmaCount": lemma_count,
            "description": manifest.get("description"),
        },
        "lemmas": lemmas,
        "items": norm_items,
        "entries": entries,
        "phrases": raw.get("phrases") or [],
    }

    (packs_dir / f"{pid}.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    pool = {
        "title": title,
        "lang": lang,
        "items": [
            {
                "text": it["text"],
                **({"hint": it["hint"]} if it.get("hint") else {}),
                **({"spell": it["spell"]} if it.get("spell") else {}),
            }
            for it in norm_items
        ]
        or [{"text": lemma} for lemma in lemmas],
    }
    (packs_dir / f"{pid}.pool.json").write_text(
        json.dumps(pool, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    glossary = {
        "manifest": pack["manifest"],
        "entries": entries,
        "phrases": [],
    }
    (packs_dir / f"{pid}.glossary.json").write_text(
        json.dumps(glossary, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    browse_items = [
        {
            "word": it["text"],
            "phonetic": it.get("spell") or "",
            "gloss": it.get("hint") or "",
            "example": "",
            "exampleTr": "",
        }
        for it in norm_items
    ] or [
        {
            "word": lemma,
            "phonetic": "",
            "gloss": "",
            "example": "",
            "exampleTr": "",
        }
        for lemma in lemmas
    ]
    browse = {"title": title, "items": browse_items}
    (packs_dir / f"{pid}.browse.json").write_text(
        json.dumps(browse, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    return {
        "id": pid,
        "title": title,
        "version": version,
        "lang": lang,
        "glossLang": gloss_lang,
        "lemmaCount": lemma_count,
        "source": "local",
        "installedAt": str(int(time.time())),
    }


def refresh_catalog_cache(wb_root: Path) -> None:
    catalog_path = ROOT / "catalog.json"
    if not catalog_path.exists():
        return
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    # Keep relative asset names — Discover can show books; install still needs local.
    catalogs = wb_root / "catalogs"
    catalogs.mkdir(parents=True, exist_ok=True)
    out = catalogs / "bubtype-official.json"
    out.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated catalog cache → {out}")

    # Clear last sync network error so UI doesn't look stuck.
    subs = wb_root / "subscriptions.json"
    if subs.exists():
        data = json.loads(subs.read_text(encoding="utf-8"))
        for feed in data.get("feeds") or []:
            if feed.get("id") == "bubtype-official":
                feed["lastError"] = None
                feed["lastSyncAt"] = str(int(time.time()))
        subs.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ids = sys.argv[1:] or DEFAULT_IDS
    wb_root = app_wordbooks_root()
    wb_root.mkdir(parents=True, exist_ok=True)
    print(f"wordbooks root: {wb_root}")

    index_path = wb_root / "index.json"
    index = {"activeId": None, "items": []}
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index.setdefault("items", [])

    by_id = {it["id"]: it for it in index["items"]}
    installed = []
    for pack_id in ids:
        try:
            entry = install_one(wb_root, pack_id)
        except FileNotFoundError:
            print(f"skip missing {pack_id}")
            continue
        by_id[entry["id"]] = entry
        installed.append(entry["id"])
        print(f"installed {entry['id']} ({entry['lemmaCount']})")

    index["items"] = list(by_id.values())
    # Prefer a CJK core pack for quick try if nothing sensible active.
    prefer = ["zh-hsk-1-3", "ja-jlpt-n5n4", "ko-core-beginner", "zh-daily-a1"]
    if not index.get("activeId") or index["activeId"] not in by_id:
        for pid in prefer:
            if pid in by_id:
                index["activeId"] = pid
                break
    elif "zh-hsk-1-3" in installed:
        index["activeId"] = "zh-hsk-1-3"

    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    refresh_catalog_cache(wb_root)
    print(f"activeId={index.get('activeId')}  installed={len(installed)}")


if __name__ == "__main__":
    main()
