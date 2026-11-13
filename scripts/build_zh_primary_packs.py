#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ZH-gloss primary packs from existing bilingual sources (no MT).

Sources:
  - es-core-a1-zh:
      CEFR A1 lemmas (Talhakasikci/cefr-vocabulary-dataset es-A1)
      × Spanish→ZH map (imabakagain/Learn_Spanish_w_Chinese spanish_vocab_8000_zh.csv)
  - ja-jlpt-n5n4:
      SeupLio/kotoba-jlpt processed N5+N4 (already has zh + romaji), MIT
  - ko-core-beginner:
      Amulopapa67/open-yonsei-korean-vocabulary vol-01 (korean+chinese), CC BY-SA 3.0
      romanization via korean_romanizer

Usage:
  python scripts/build_zh_primary_packs.py
  python scripts/build_zh_primary_packs.py --only es,ja,ko --refresh
"""
from __future__ import annotations

import argparse
import csv
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

SOURCES = {
    "es-A1.json": "repos/Talhakasikci/cefr-vocabulary-dataset/contents/vocab_json/es-A1.json",
    "es-zh-8000.csv": "repos/imabakagain/Learn_Spanish_w_Chinese/contents/spanish_vocab_8000_zh.csv",
    "kotoba-n5.json": "repos/SeupLio/kotoba-jlpt/contents/data/processed/n5.json",
    "kotoba-n4.json": "repos/SeupLio/kotoba-jlpt/contents/data/processed/n4.json",
    "yonsei-vol01.json": "repos/Amulopapa67/open-yonsei-korean-vocabulary/contents/data/json/vol-01.json",
}

PREFERRED_TAIL = [
    "fr-core-a1-zh",
    "fr-daily-a1-zh",
    "es-core-a1-zh",
    "es-daily-a1-zh",
    "zh-daily-a1",
    "zh-hsk-1-3",
    "ja-daily-a1",
    "ja-jlpt-n5n4",
    "ko-daily-a1-zh",
    "ko-core-beginner",
]


def gh_token() -> str | None:
    env = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()
    if env:
        return env
    try:
        out = subprocess.check_output(
            ["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL
        )
        return out.strip() or None
    except Exception:
        return None


def download_github_raw(api_path: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    token = gh_token()
    if not token:
        raise SystemExit("Need GH_TOKEN or `gh auth login`")
    req = urllib.request.Request(
        f"https://api.github.com/{api_path}",
        headers={
            "User-Agent": "bubtype-packs-gen/1.2",
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    print(f"downloaded {dest.name} ({dest.stat().st_size} bytes)")


def ensure_sources(refresh: bool, need: set[str]) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    want_names: list[str] = []
    if "es" in need:
        want_names += ["es-A1.json", "es-zh-8000.csv"]
    if "ja" in need:
        want_names += ["kotoba-n5.json", "kotoba-n4.json"]
    if "ko" in need:
        want_names += ["yonsei-vol01.json"]
    for name in want_names:
        path = CACHE / name
        if refresh or not path.exists() or path.stat().st_size < 500:
            download_github_raw(SOURCES[name], path)


def clean_hint(text: str, *, max_len: int = 48) -> str:
    t = re.sub(r"<[^>]+>", "", text or "")
    t = re.sub(r"\s+", " ", t).strip(" ;,，、。.")
    if "；" in t:
        t = t.split("；", 1)[0].strip()
    if ";" in t and re.search(r"[\u4e00-\u9fff]", t):
        # keep Chinese side short: first chunk
        t = t.split(";", 1)[0].strip()
    if len(t) > max_len:
        t = t[: max_len - 1].rstrip(" ;,，、") + "…"
    return t


def write_items_pack(
    pack_id: str,
    *,
    title: str,
    lang: str,
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
            "glossLang": "zh",
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
        "glossLang": "zh",
        "lemmaCount": len(items),
        "description": description,
        "asset": out.name,
    }


def write_lemma_pack(
    pack_id: str,
    *,
    title: str,
    lang: str,
    description: str,
    version: str,
    lemmas: list[str],
    entries: list[dict],
    source: str,
) -> dict:
    payload = {
        "manifest": {
            "id": pack_id,
            "title": title,
            "version": version,
            "lang": lang,
            "glossLang": "zh",
            "source": source,
            "lemmaCount": len(lemmas),
            "description": description,
        },
        "lemmas": lemmas,
        "entries": entries,
        "phrases": [],
    }
    out = ROOT / f"{pack_id}-v1.json"
    out.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.name} ({len(lemmas)} lemmas)")
    return {
        "id": pack_id,
        "title": title,
        "version": version,
        "lang": lang,
        "glossLang": "zh",
        "lemmaCount": len(lemmas),
        "description": description,
        "asset": out.name,
    }


# Editorial ZH for CEFR A1 lemmas missing from the 8000 frequency list.
ES_ZH_EXTRA: dict[str, str] = {
    "aire acondicionado": "空调",
    "ama de casa": "家庭主妇",
    "antipático": "不友善的",
    "aparcamiento": "停车场",
    "arroba": "@（艾特）",
    "bañarse": "洗澡；游泳",
    "bocadillo": "西班牙三明治",
    "bolígrafo": "圆珠笔",
    "bombero": "消防员",
    "budista": "佛教的；佛教徒",
    "carné de conducir": "驾驶证",
    "catedral": "大教堂",
    "céntrico": "市中心的",
    "código postal": "邮政编码",
    "comprador": "买家",
    "comunicado": "声明；公告",
    "correo electrónico": "电子邮件",
    "de ida": "单程的",
    "dedicarse a": "从事",
    "diccionario": "词典",
    "divorciado": "离婚的",
    "ducharse": "淋浴",
    "enfermero": "护士",
    "esquiar": "滑雪",
    "estantería": "书架；货架",
    "estado civil": "婚姻状况",
    "euro": "欧元",
    "fotocopia": "复印件",
    "individual": "单人的；个人的",
    "lavabo": "洗手池",
    "llamarse": "名叫",
    "lugar de nacimiento": "出生地",
    "marroquí": "摩洛哥的；摩洛哥人",
    "merendar": "吃点心；吃下午茶",
    "merienda": "下午点心",
    "moreno": "黑发的；肤色偏深的",
    "musulmán": "穆斯林的；穆斯林",
    "nacionalidad": "国籍",
    "nevar": "下雪",
    "paella": "西班牙海鲜饭",
    "página web": "网页",
    "pizarra": "黑板",
    "que": "那；什么（关系代词）",
    "quiosco": "报亭；小卖亭",
    "sala de estar": "客厅",
    "sillón": "扶手椅",
    "sociable": "爱社交的",
    "tarjeta de crédito": "信用卡",
    "taxista": "出租车司机",
    "terraza": "露台；阳台",
    "tinto": "红葡萄酒",
    "tortilla": "西班牙土豆饼；玉米饼",
    "turismo": "旅游",
    "turista": "游客",
    "verdura": "蔬菜",
    "viudo": "丧偶的；鳏夫",
    "y": "和",
}


def load_es_zh_map() -> dict[str, str]:
    path = CACHE / "es-zh-8000.csv"
    raw = path.read_bytes()
    text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig")
    out: dict[str, str] = {}
    for row in csv.reader(text.splitlines()):
        if len(row) < 2:
            continue
        lemma, zh = row[0].strip(), clean_hint(row[1])
        if not lemma or not zh or len(lemma) <= 1:
            continue
        # Prefer first occurrence (higher frequency in this list).
        out.setdefault(lemma.casefold(), zh)
    for lemma, zh in ES_ZH_EXTRA.items():
        out[lemma.casefold()] = clean_hint(zh)
    return out


def build_es() -> dict:
    rows = json.loads((CACHE / "es-A1.json").read_text(encoding="utf-8"))
    zh_map = load_es_zh_map()
    by_lemma: dict[str, dict] = {}
    for row in rows:
        lemma = str(row.get("lemma") or "").strip()
        if not lemma:
            continue
        by_lemma.setdefault(lemma.casefold(), row)

    lemmas: list[str] = []
    entries: list[dict] = []
    miss: list[str] = []
    for key in sorted(by_lemma):
        row = by_lemma[key]
        lemma = str(row.get("lemma") or "").strip()
        zh = zh_map.get(key)
        if not zh:
            miss.append(lemma)
            continue
        lemmas.append(lemma)
        entry: dict = {
            "lemma": lemma,
            "display": lemma,
            "senses": [{"pos": str(row.get("pos") or "other"), "gloss": zh}],
        }
        if row.get("ipa"):
            entry["ipa"] = str(row["ipa"])
        entries.append(entry)
    print(f"  es A1 join: {len(lemmas)} hit, {len(miss)} miss")
    if miss:
        print("  still missing:", ", ".join(miss))
    return write_lemma_pack(
        "es-core-a1-zh",
        title="西语 A1 核心",
        lang="es",
        description="西班牙语入门核心词 · 中文释义（CEFR A1 × 西语常用词中文表）",
        version="1.1.1",
        lemmas=lemmas,
        entries=entries,
        source="cefr-es-a1+es-zh-8000",
    )


def build_ja() -> dict:
    items: list[dict] = []
    seen: set[str] = set()
    for fname in ("kotoba-n5.json", "kotoba-n4.json"):
        rows = json.loads((CACHE / fname).read_text(encoding="utf-8"))
        for w in rows:
            text = (w.get("word") or "").strip()
            spell = (w.get("romaji") or "").strip().lower()
            zh_list = w.get("zh") or []
            if isinstance(zh_list, str):
                zh_list = [zh_list]
            hint = clean_hint("；".join(str(x) for x in zh_list if x))
            if not text or not spell or not hint or text in seen:
                continue
            seen.add(text)
            items.append({"text": text, "hint": hint, "kind": "phrase", "spell": spell})
    return write_items_pack(
        "ja-jlpt-n5n4",
        title="日语 JLPT N5–N4",
        lang="ja",
        description="JLPT N5+N4 常用词 · 中文释义（罗马字拼写）",
        version="1.1.0",
        items=items,
        source="kotoba-jlpt",
    )


def hangul_to_romaja(text: str) -> str:
    from korean_romanizer.romanizer import Romanizer

    raw = Romanizer(text).romanize()
    # Typing-friendly: lower, drop hyphen syllable breaks.
    return re.sub(r"\s+", " ", (raw or "").replace("-", "").strip().lower())


def build_ko() -> dict:
    payload = json.loads((CACHE / "yonsei-vol01.json").read_text(encoding="utf-8"))
    rows = payload.get("rows") or []
    items: list[dict] = []
    seen: set[str] = set()
    for w in rows:
        if str(w.get("entry_kind") or "") == "grammar":
            continue
        text = (w.get("korean") or "").strip()
        hint = clean_hint(str(w.get("chinese") or ""))
        if not text or not hint or text in seen:
            continue
        # Skip very long expressions for core typing pack.
        if len(text) > 24:
            continue
        try:
            spell = hangul_to_romaja(text)
        except Exception:
            spell = ""
        if not spell:
            continue
        seen.add(text)
        items.append({"text": text, "hint": hint, "kind": "phrase", "spell": spell})
    return write_items_pack(
        "ko-core-beginner",
        title="韩语入门核心",
        lang="ko",
        description="韩语入门高频词 · 中文释义（《延世韩国语》第一册开源词表）",
        version="1.1.0",
        items=items,
        source="open-yonsei-vol1",
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
    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"updated catalog ({len(ordered)} books)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", default="es,ja,ko")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    need = {x.strip() for x in args.only.split(",") if x.strip()}
    ensure_sources(args.refresh, need)
    built: list[dict] = []
    if "es" in need:
        print("== es-core-a1-zh ==")
        built.append(build_es())
    if "ja" in need:
        print("== ja-jlpt-n5n4 ==")
        built.append(build_ja())
    if "ko" in need:
        print("== ko-core-beginner ==")
        built.append(build_ko())
    update_catalog(built)
    for b in built:
        print(f"  {b['id']}: {b['lemmaCount']} · glossLang={b['glossLang']}")


if __name__ == "__main__":
    main()
