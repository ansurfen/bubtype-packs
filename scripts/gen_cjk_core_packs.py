#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build larger ZH / JA / KO core packs with romanization (`spell`) for BubType.

Sources (downloaded into `_cache/`, not committed):
  - HSK 3.0 words — HearMandarin (CC BY 4.0)
  - OpenJLPT N5+N4 vocab — evanclan/OpenJLPT (CC BY-SA 4.0)
  - Korean flashcards beginner set — niksavis/korean-flashcards (MIT)

Usage:
  python scripts/gen_cjk_core_packs.py
  # re-fetch sources:
  python scripts/gen_cjk_core_packs.py --refresh

Requires network on first run. GitHub raw assets use GH_TOKEN / `gh auth token` when
cdn.jsdelivr / raw.githubusercontent.com are blocked.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "_cache"
CATALOG_PATH = ROOT / "catalog.json"

HSK_URL = "https://hearmandarin.com/datasets/hsk-3-0-words.json"
GH_RAW = {
    "jlpt-n5.json": "repos/evanclan/OpenJLPT/contents/data/json/vocab/n5.json",
    "jlpt-n4.json": "repos/evanclan/OpenJLPT/contents/data/json/vocab/n4.json",
    "ko-flashcards.json": "repos/niksavis/korean-flashcards/contents/data/korean-words.json",
}

# Prefer these ids near the multilingual daily packs in catalog order.
PREFERRED_TAIL = [
    "fr-core-a1-zh",
    "fr-daily-a1-zh",
    "zh-daily-a1",
    "zh-hsk-1-3",
    "ja-daily-a1",
    "ja-jlpt-n5n4",
    "ko-daily-a1-zh",
    "ko-core-beginner",
    "es-daily-a1-zh",
]


def gh_token() -> str | None:
    env = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()
    if env:
        return env
    try:
        out = subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL)
        return out.strip() or None
    except Exception:
        return None


def download(url: str, dest: Path, *, github_api: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "bubtype-packs-gen/1.0"}
    token = gh_token()
    if github_api:
        if not token:
            raise SystemExit("GitHub download needs GH_TOKEN or `gh auth login`")
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github.raw"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    print(f"downloaded {dest.name} ({dest.stat().st_size} bytes)")


def ensure_sources(refresh: bool) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    hsk = CACHE / "hsk-3-0-words.json"
    if refresh or not hsk.exists():
        download(HSK_URL, hsk)
    for name, api_path in GH_RAW.items():
        path = CACHE / name
        if refresh or not path.exists() or path.stat().st_size < 1000:
            download(f"https://api.github.com/{api_path}", path, github_api=True)


def clean_hint(text: str, *, max_len: int = 80) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    if len(t) > max_len:
        t = t[: max_len - 1].rstrip(" ;,/") + "…"
    return t


def norm_romaja(s: str) -> str:
    # Flashcards use hyphens as syllable breaks; typing works better without them.
    return re.sub(r"\s+", " ", (s or "").replace("-", "").strip().lower())


# Tone-number → diacritic (standard pinyin vowel priority).
_TONE_VOWELS = {
    "a": "āáǎàa",
    "e": "ēéěèe",
    "i": "īíǐìi",
    "o": "ōóǒòo",
    "u": "ūúǔùu",
    "ü": "ǖǘǚǜü",
    "v": "ǖǘǚǜü",  # CEDICT-style ü
}


def numbered_syllable_to_tone(syl: str) -> str:
    """Convert one syllable like 'xue2' / 'nv3' to tone-marked form."""
    s = (syl or "").strip().replace("u:", "ü").replace("U:", "Ü")
    m = re.match(r"^([A-Za-züÜ]+)([1-5])$", s)
    if not m:
        return s
    base, tone_s = m.group(1), m.group(2)
    tone = int(tone_s)
    if tone == 5:
        return base.replace("v", "ü").replace("V", "Ü")
    lower = base.lower()
    # Pick vowel to mark: a/e first, else last o/u, else last vowel.
    mark_at = None
    for ch in ("a", "e"):
        idx = lower.find(ch)
        if idx >= 0:
            mark_at = idx
            break
    if mark_at is None:
        for idx in range(len(lower) - 1, -1, -1):
            if lower[idx] in "ou":
                mark_at = idx
                break
    if mark_at is None:
        for idx in range(len(lower) - 1, -1, -1):
            if lower[idx] in "iüv":
                mark_at = idx
                break
    if mark_at is None:
        return base
    vowel = lower[mark_at]
    marked = _TONE_VOWELS[vowel][tone - 1]
    # Preserve original casing of the vowel slot loosely (always lower diacritic).
    out = list(base.replace("v", "ü").replace("V", "Ü"))
    # Recompute index on replaced string
    lower2 = "".join(out).lower()
    mark_at = None
    for ch in ("a", "e"):
        idx = lower2.find(ch)
        if idx >= 0:
            mark_at = idx
            break
    if mark_at is None:
        for idx in range(len(lower2) - 1, -1, -1):
            if lower2[idx] in "ou":
                mark_at = idx
                break
    if mark_at is None:
        for idx in range(len(lower2) - 1, -1, -1):
            if lower2[idx] in "iü":
                mark_at = idx
                break
    if mark_at is None:
        return "".join(out)
    out[mark_at] = marked
    return "".join(out)


def hsk_spell(pinyin: str | None, pinyin_num: str | None) -> str:
    """Prefer spaced tone-mark pinyin; split glued numbered forms when needed."""
    marked = re.sub(r"\s+", " ", (pinyin or "").strip())
    numbered = re.sub(r"\s+", " ", (pinyin_num or "").strip())
    if marked and " " in marked:
        return marked
    # Split glued numbered pinyin (xue2sheng1 → xué shēng).
    if numbered:
        parts = re.findall(r"[A-Za-züÜ:]+[1-5]", numbered.replace(" ", ""))
        if len(parts) >= 1:
            return " ".join(numbered_syllable_to_tone(p) for p in parts)
    return marked or numbered


def write_pack(
    pack_id: str,
    *,
    title: str,
    lang: str,
    gloss_lang: str,
    description: str,
    version: str,
    items: list[dict],
    source: str,
) -> dict:
    payload = {
        "manifest": {
            "id": pack_id,
            "title": title,
            "version": version,
            "lang": lang,
            "glossLang": gloss_lang,
            "source": source,
            "lemmaCount": len(items),
            "description": description,
        },
        "items": items,
    }
    out = ROOT / f"{pack_id}-v1.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.name} ({len(items)} items)")
    return {
        "id": pack_id,
        "title": title,
        "version": version,
        "lang": lang,
        "glossLang": gloss_lang,
        "lemmaCount": len(items),
        "description": description,
        "asset": out.name,
    }


def build_zh_hsk() -> dict:
    raw = json.loads((CACHE / "hsk-3-0-words.json").read_text(encoding="utf-8"))
    words = raw["words"] if isinstance(raw, dict) else raw
    bands = {1, 2, 3}
    items: list[dict] = []
    seen: set[str] = set()
    # Stable order: band then syllabus sequence.
    rows = [
        w
        for w in words
        if w.get("hsk3_band") in bands and (w.get("simplified") or "").strip()
    ]
    rows.sort(key=lambda w: (int(w.get("hsk3_band") or 99), int(w.get("hsk3_seq") or 10**9)))
    for w in rows:
        text = str(w["simplified"]).strip()
        if text in seen:
            continue
        spell = hsk_spell(w.get("pinyin"), w.get("pinyin_num"))
        if not spell:
            continue
        hint = clean_hint(str(w.get("gloss_en") or ""))
        if not hint:
            continue
        seen.add(text)
        items.append({"text": text, "hint": hint, "kind": "phrase", "spell": spell})
    return write_pack(
        "zh-hsk-1-3",
        title="中文 HSK 1–3",
        lang="zh",
        gloss_lang="en",
        description="HSK 3.0 第 1–3 级核心词 · 英文释义（拼音输入）",
        version="1.0.0",
        items=items,
        source="hsk3-hearmandarin",
    )


def build_ja_jlpt() -> dict:
    items: list[dict] = []
    seen: set[str] = set()
    for level, fname in (("N5", "jlpt-n5.json"), ("N4", "jlpt-n4.json")):
        rows = json.loads((CACHE / fname).read_text(encoding="utf-8"))
        for w in rows:
            text = (w.get("word") or "").strip()
            spell = (w.get("romaji") or "").strip().lower()
            if not text or not spell or text in seen:
                continue
            meanings = w.get("meanings") or []
            if isinstance(meanings, str):
                meanings = [meanings]
            hint = clean_hint("; ".join(str(m) for m in meanings if m))
            if not hint:
                continue
            seen.add(text)
            items.append({"text": text, "hint": hint, "kind": "phrase", "spell": spell})
    return write_pack(
        "ja-jlpt-n5n4",
        title="日语 JLPT N5–N4",
        lang="ja",
        gloss_lang="en",
        description="JLPT N5+N4 常用词 · 英文释义（罗马字拼写）",
        version="1.0.0",
        items=items,
        source="openjlpt",
    )


def build_ko_beginner() -> dict:
    raw = json.loads((CACHE / "ko-flashcards.json").read_text(encoding="utf-8"))
    words = raw["words"] if isinstance(raw, dict) else raw
    items: list[dict] = []
    seen: set[str] = set()
    rows = [w for w in words if str(w.get("difficulty") or "").lower() == "beginner"]
    rows.sort(key=lambda w: int(w.get("position") or w.get("id") or 10**9))
    for w in rows:
        text = (w.get("hangul") or "").strip()
        spell = norm_romaja(str(w.get("romanization") or ""))
        if not text or not spell or text in seen:
            continue
        hint = clean_hint(str(w.get("english") or ""))
        if not hint:
            continue
        seen.add(text)
        items.append({"text": text, "hint": hint, "kind": "phrase", "spell": spell})
    return write_pack(
        "ko-core-beginner",
        title="韩语入门核心",
        lang="ko",
        gloss_lang="en",
        description="韩语入门高频词 · 英文释义（罗马音拼写）",
        version="1.0.0",
        items=items,
        source="korean-flashcards",
    )


def update_catalog(books: list[dict]) -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    by_id = {b["id"]: b for b in catalog.get("books", [])}
    for b in books:
        by_id[b["id"]] = b

    preferred_head = [
        "oxford-3000-zh",
        "oxford-5000-zh",
        "oxford-3000-en",
        "oxford-5000-en",
        "oxford-3000-ja",
        "oxford-5000-ja",
        "rant-workplace",
        "rant-campus",
        "rant-invest",
        "rant-ecommerce",
    ]
    ordered: list[dict] = []
    seen: set[str] = set()
    for pid in preferred_head + PREFERRED_TAIL:
        if pid in by_id and pid not in seen:
            ordered.append(by_id[pid])
            seen.add(pid)
    for pid, book in by_id.items():
        if pid not in seen:
            ordered.append(book)
            seen.add(pid)

    catalog["books"] = ordered
    catalog["updatedAt"] = date.today().isoformat()
    catalog["source"] = catalog.get("source") or "https://github.com/ansurfen/bubtype-packs"
    catalog["version"] = catalog.get("version") or 1
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated catalog ({len(ordered)} books)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="Re-download source dumps")
    args = ap.parse_args()
    ensure_sources(args.refresh)
    built = [build_zh_hsk(), build_ja_jlpt(), build_ko_beginner()]
    update_catalog(built)
    for b in built:
        print(f"  {b['id']}: {b['lemmaCount']} lemmas")


if __name__ == "__main__":
    main()
