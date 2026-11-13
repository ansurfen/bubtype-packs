#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 pack expansion for Chinese learners of other languages.

Builds / refreshes:
  - fr-daily-a1-zh, es-daily-a1-zh  (thickened curated daily)
  - ja-jlpt-n3                      (kotoba-jlpt N3, ZH)
  - ko-yonsei-2, ko-yonsei-3        (Open Yonsei vols 2–3)
  - de-core-a1-zh                   (CEFR/Goethe A1 × DE–ZH vocab)

Usage:
  python scripts/expand_p1_packs.py
  python scripts/expand_p1_packs.py --only daily,ja,ko,de --refresh
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
    "kotoba-n3.json": "repos/SeupLio/kotoba-jlpt/contents/data/processed/n3.json",
    "yonsei-vol02.json": "repos/Amulopapa67/open-yonsei-korean-vocabulary/contents/data/json/vol-02.json",
    "yonsei-vol03.json": "repos/Amulopapa67/open-yonsei-korean-vocabulary/contents/data/json/vol-03.json",
    "de-A1.json": "repos/Talhakasikci/cefr-vocabulary-dataset/contents/vocab_json/de-A1.json",
    "german_vocab.csv": "repos/ShaoWanqiu/German-Vocabulary-Master/contents/backend/german_vocab.csv",
}

PREFERRED_TAIL = [
    "fr-core-a1-zh",
    "fr-daily-a1-zh",
    "es-core-a1-zh",
    "es-daily-a1-zh",
    "de-core-a1-zh",
    "zh-daily-a1",
    "zh-hsk-1-3",
    "ja-daily-a1",
    "ja-jlpt-n5n4",
    "ja-jlpt-n3",
    "ko-daily-a1-zh",
    "ko-core-beginner",
    "ko-yonsei-2",
    "ko-yonsei-3",
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
            "User-Agent": "bubtype-packs-gen/1.3",
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    print(f"downloaded {dest.name} ({dest.stat().st_size} bytes)")


def ensure_sources(refresh: bool, need: set[str]) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    want: list[str] = []
    if "ja" in need:
        want.append("kotoba-n3.json")
    if "ko" in need:
        want += ["yonsei-vol02.json", "yonsei-vol03.json"]
    if "de" in need:
        want += ["de-A1.json", "german_vocab.csv"]
    for name in want:
        path = CACHE / name
        if refresh or not path.exists() or path.stat().st_size < 500:
            download_github_raw(SOURCES[name], path)


def clean_hint(text: str, *, max_len: int = 48) -> str:
    t = re.sub(r"<[^>]+>", "", text or "")
    t = re.sub(r"\s+", " ", t).strip(" ;,，、。.")
    if "；" in t:
        t = t.split("；", 1)[0].strip()
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


def item(text: str, hint: str, kind: str, spell: str | None = None) -> dict:
    out = {"text": text, "hint": hint, "kind": kind}
    if spell:
        out["spell"] = spell
    return out


def strip_accents(s: str) -> str:
    table = str.maketrans(
        "áéíóúüñÁÉÍÓÚÜÑàâäèêëìîïòôöùûüçÀÂÄÈÊËÌÎÏÒÔÖÙÛÜÇ",
        "aeiouunAEIOUUNaaaeeeiiiooouuucAAAEEEIIIOOOUUUC",
    )
    return s.translate(table)


# --- Daily thicken (extra words + sentences beyond original 64) ---
ES_EXTRA_WORDS = [
    ("hotel", "酒店", "hotel"),
    ("aeropuerto", "机场", "aeropuerto"),
    ("billete", "票", "billete"),
    ("pasaporte", "护照", "pasaporte"),
    ("maleta", "行李箱", "maleta"),
    ("taxi", "出租车", "taxi"),
    ("metro", "地铁", "metro"),
    ("autobús", "公交车", "autobus"),
    ("calle", "街道", "calle"),
    ("plaza", "广场", "plaza"),
    ("tienda", "商店", "tienda"),
    ("supermercado", "超市", "supermercado"),
    ("farmacia", "药店", "farmacia"),
    ("hospital", "医院", "hospital"),
    ("médico", "医生", "medico"),
    ("enfermo", "生病的", "enfermo"),
    ("dinero", "钱", "dinero"),
    ("tarjeta", "卡", "tarjeta"),
    ("precio", "价格", "precio"),
    ("barato", "便宜的", "barato"),
    ("caro", "贵的", "caro"),
    ("abrir", "打开", "abrir"),
    ("cerrar", "关闭", "cerrar"),
    ("entrar", "进入", "entrar"),
    ("salir", "出去；离开", "salir"),
    ("esperar", "等待", "esperar"),
    ("llamar", "打电话；叫", "llamar"),
    ("necesitar", "需要", "necesitar"),
    ("querer", "想要", "querer"),
    ("poder", "能够", "poder"),
    ("saber", "知道", "saber"),
    ("entender", "明白", "entender"),
    ("comprar", "买", "comprar"),
    ("vender", "卖", "vender"),
    ("pagar", "付钱", "pagar"),
    ("reservar", "预订", "reservar"),
    ("desayuno", "早餐", "desayuno"),
    ("almuerzo", "午餐", "almuerzo"),
    ("cena", "晚餐", "cena"),
    ("cerveza", "啤酒", "cerveza"),
    ("vino", "葡萄酒", "vino"),
    ("fruta", "水果", "fruta"),
    ("carne", "肉", "carne"),
    ("pescado", "鱼", "pescado"),
    ("vegetales", "蔬菜", "vegetales"),
    ("pan", "面包", "pan"),
    ("leche", "牛奶", "leche"),
    ("azúcar", "糖", "azucar"),
    ("sal", "盐", "sal"),
    ("grande", "大的", "grande"),
    ("pequeño", "小的", "pequeno"),
    ("nuevo", "新的", "nuevo"),
    ("viejo", "旧的；老的", "viejo"),
    ("bonito", "漂亮的", "bonito"),
    ("fácil", "简单的", "facil"),
    ("difícil", "难的", "dificil"),
    ("cerca", "附近", "cerca"),
    ("lejos", "远", "lejos"),
    ("izquierda", "左边", "izquierda"),
    ("derecha", "右边", "derecha"),
    ("aquí", "这里", "aqui"),
    ("allí", "那里", "alli"),
    ("ahora", "现在", "ahora"),
    ("luego", "然后；稍后", "luego"),
    ("siempre", "总是", "siempre"),
    ("nunca", "从不", "nunca"),
    ("también", "也", "tambien"),
    ("muy", "很", "muy"),
    ("más", "更多", "mas"),
    ("menos", "更少", "menos"),
]

ES_EXTRA_SENTS = [
    ("Necesito un taxi", "我需要一辆出租车", "Necesito un taxi"),
    ("¿Cuánto cuesta esto?", "这个多少钱？", "Cuanto cuesta esto?"),
    ("Quiero reservar una habitación", "我想订一间房", "Quiero reservar una habitacion"),
    ("¿Dónde está el baño?", "厕所在哪里？", "Donde esta el bano?"),
    ("Estoy perdido", "我迷路了", "Estoy perdido"),
    ("¿Habla inglés?", "你会说英语吗？", "Habla ingles?"),
    ("No hablo español muy bien", "我西班牙语说得不太好", "No hablo espanol muy bien"),
    ("¿Puede ayudarme?", "您能帮我吗？", "Puede ayudarme?"),
    ("Voy al aeropuerto", "我去机场", "Voy al aeropuerto"),
    ("El tren sale a las tres", "火车三点发车", "El tren sale a las tres"),
    ("Me duele la cabeza", "我头疼", "Me duele la cabeza"),
    ("Necesito ver a un médico", "我需要看医生", "Necesito ver a un medico"),
    ("¿Está lejos?", "远吗？", "Esta lejos?"),
    ("Está a la derecha", "在右边", "Esta a la derecha"),
    ("Quiero pagar con tarjeta", "我想用卡支付", "Quiero pagar con tarjeta"),
    ("¿Aceptan efectivo?", "收现金吗？", "Aceptan efectivo?"),
    ("Una mesa para dos, por favor", "请给我两人桌", "Una mesa para dos, por favor"),
    ("Está delicioso", "很好吃", "Esta delicioso"),
    ("No como carne", "我不吃肉", "No como carne"),
    ("¿Tiene wifi?", "有无线网吗？", "Tiene wifi?"),
    ("La contraseña, por favor", "请告诉我密码", "La contrasena, por favor"),
    ("Voy de compras", "我去购物", "Voy de compras"),
    ("Busco una camisa", "我在找一件衬衫", "Busco una camisa"),
    ("¿Puedo cambiarlo?", "可以换吗？", "Puedo cambiarlo?"),
    ("Tengo una reserva", "我有预订", "Tengo una reserva"),
    ("A qué hora abre?", "几点开门？", "A que hora abre?"),
    ("Cierra a las nueve", "九点关门", "Cierra a las nueve"),
    ("Hace frío hoy", "今天很冷", "Hace frio hoy"),
    ("Hace calor", "很热", "Hace calor"),
    ("Llueve mucho", "雨下得很大", "Llueve mucho"),
    ("Me llamo Ana", "我叫 Ana", "Me llamo Ana"),
    ("Soy de China", "我来自中国", "Soy de China"),
    ("Vivo en Madrid", "我住在马德里", "Vivo en Madrid"),
    ("Trabajo en una oficina", "我在办公室工作", "Trabajo en una oficina"),
    ("Estudio español", "我学西班牙语", "Estudio espanol"),
    ("Nos vemos luego", "回头见", "Nos vemos luego"),
    ("Feliz cumpleaños", "生日快乐", "Feliz cumpleanos"),
    ("Buena suerte", "祝你好运", "Buena suerte"),
    ("Que te mejores", "祝你早日康复", "Que te mejores"),
    ("Con permiso", "借过；不好意思", "Con permiso"),
]

FR_EXTRA_WORDS = [
    ("hôtel", "酒店", "hotel"),
    ("aéroport", "机场", "aeroport"),
    ("billet", "票", "billet"),
    ("passeport", "护照", "passeport"),
    ("valise", "行李箱", "valise"),
    ("taxi", "出租车", "taxi"),
    ("métro", "地铁", "metro"),
    ("bus", "公交车", "bus"),
    ("rue", "街道", "rue"),
    ("place", "广场；地方", "place"),
    ("magasin", "商店", "magasin"),
    ("supermarché", "超市", "supermarche"),
    ("pharmacie", "药店", "pharmacie"),
    ("hôpital", "医院", "hopital"),
    ("médecin", "医生", "medecin"),
    ("malade", "生病的", "malade"),
    ("argent", "钱", "argent"),
    ("carte", "卡；地图", "carte"),
    ("prix", "价格", "prix"),
    ("bon marché", "便宜", "bon marche"),
    ("cher", "贵的", "cher"),
    ("ouvrir", "打开", "ouvrir"),
    ("fermer", "关闭", "fermer"),
    ("entrer", "进入", "entrer"),
    ("sortir", "出去", "sortir"),
    ("attendre", "等待", "attendre"),
    ("appeler", "打电话；叫", "appeler"),
    ("avoir besoin", "需要", "avoir besoin"),
    ("vouloir", "想要", "vouloir"),
    ("pouvoir", "能够", "pouvoir"),
    ("savoir", "知道", "savoir"),
    ("comprendre", "明白", "comprendre"),
    ("acheter", "买", "acheter"),
    ("vendre", "卖", "vendre"),
    ("payer", "付钱", "payer"),
    ("réserver", "预订", "reserver"),
    ("petit-déjeuner", "早餐", "petit-dejeuner"),
    ("déjeuner", "午餐", "dejeuner"),
    ("dîner", "晚餐", "diner"),
    ("bière", "啤酒", "biere"),
    ("vin", "葡萄酒", "vin"),
    ("fruit", "水果", "fruit"),
    ("viande", "肉", "viande"),
    ("poisson", "鱼", "poisson"),
    ("légume", "蔬菜", "legume"),
    ("lait", "牛奶", "lait"),
    ("sucre", "糖", "sucre"),
    ("sel", "盐", "sel"),
    ("grand", "大的", "grand"),
    ("petit", "小的", "petit"),
    ("nouveau", "新的", "nouveau"),
    ("vieux", "旧的；老的", "vieux"),
    ("beau", "漂亮的", "beau"),
    ("facile", "简单的", "facile"),
    ("difficile", "难的", "difficile"),
    ("près", "附近", "pres"),
    ("loin", "远", "loin"),
    ("gauche", "左边", "gauche"),
    ("droite", "右边", "droite"),
    ("ici", "这里", "ici"),
    ("là", "那里", "la"),
    ("maintenant", "现在", "maintenant"),
    ("après", "之后", "apres"),
    ("toujours", "总是", "toujours"),
    ("jamais", "从不", "jamais"),
    ("aussi", "也", "aussi"),
    ("très", "很", "tres"),
    ("plus", "更多", "plus"),
    ("moins", "更少", "moins"),
]

FR_EXTRA_SENTS = [
    ("J'ai besoin d'un taxi", "我需要一辆出租车", "J'ai besoin d'un taxi"),
    ("Ça coûte combien ?", "这个多少钱？", "Ca coute combien ?"),
    ("Je voudrais réserver une chambre", "我想订一间房", "Je voudrais reserver une chambre"),
    ("Où sont les toilettes ?", "厕所在哪里？", "Ou sont les toilettes ?"),
    ("Je suis perdu", "我迷路了", "Je suis perdu"),
    ("Parlez-vous anglais ?", "你会说英语吗？", "Parlez-vous anglais ?"),
    ("Je ne parle pas très bien français", "我法语说得不太好", "Je ne parle pas tres bien francais"),
    ("Pouvez-vous m'aider ?", "您能帮我吗？", "Pouvez-vous m'aider ?"),
    ("Je vais à l'aéroport", "我去机场", "Je vais a l'aeroport"),
    ("Le train part à trois heures", "火车三点发车", "Le train part a trois heures"),
    ("J'ai mal à la tête", "我头疼", "J'ai mal a la tete"),
    ("Je dois voir un médecin", "我需要看医生", "Je dois voir un medecin"),
    ("C'est loin ?", "远吗？", "C'est loin ?"),
    ("C'est à droite", "在右边", "C'est a droite"),
    ("Je veux payer par carte", "我想用卡支付", "Je veux payer par carte"),
    ("Vous acceptez les espèces ?", "收现金吗？", "Vous acceptez les especes ?"),
    ("Une table pour deux, s'il vous plaît", "请给我两人桌", "Une table pour deux, s'il vous plait"),
    ("C'est délicieux", "很好吃", "C'est delicieux"),
    ("Je ne mange pas de viande", "我不吃肉", "Je ne mange pas de viande"),
    ("Vous avez le wifi ?", "有无线网吗？", "Vous avez le wifi ?"),
    ("Le mot de passe, s'il vous plaît", "请告诉我密码", "Le mot de passe, s'il vous plait"),
    ("Je vais faire des courses", "我去购物", "Je vais faire des courses"),
    ("Je cherche une chemise", "我在找一件衬衫", "Je cherche une chemise"),
    ("Je peux l'échanger ?", "可以换吗？", "Je peux l'echanger ?"),
    ("J'ai une réservation", "我有预订", "J'ai une reservation"),
    ("À quelle heure ouvrez-vous ?", "几点开门？", "A quelle heure ouvrez-vous ?"),
    ("Ça ferme à neuf heures", "九点关门", "Ca ferme a neuf heures"),
    ("Il fait froid aujourd'hui", "今天很冷", "Il fait froid aujourd'hui"),
    ("Il fait chaud", "很热", "Il fait chaud"),
    ("Il pleut beaucoup", "雨下得很大", "Il pleut beaucoup"),
    ("Je m'appelle Marie", "我叫 Marie", "Je m'appelle Marie"),
    ("Je viens de Chine", "我来自中国", "Je viens de Chine"),
    ("J'habite à Paris", "我住在巴黎", "J'habite a Paris"),
    ("Je travaille dans un bureau", "我在办公室工作", "Je travaille dans un bureau"),
    ("J'apprends le français", "我学法语", "J'apprends le francais"),
    ("À tout à l'heure", "回头见", "A tout a l'heure"),
    ("Joyeux anniversaire", "生日快乐", "Joyeux anniversaire"),
    ("Bonne chance", "祝你好运", "Bonne chance"),
    ("Prompt rétablissement", "祝你早日康复", "Prompt retablissement"),
    ("Pardon, excusez-moi", "借过；不好意思", "Pardon, excusez-moi"),
]


def load_existing_daily(pack_id: str) -> list[dict]:
    path = ROOT / f"{pack_id}-v1.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("items") or [])


def thicken_daily(pack_id: str, extras: list[tuple[str, str, str]], *, title: str, lang: str, description: str) -> dict:
    existing = load_existing_daily(pack_id)
    seen = {(it.get("text") or "").strip() for it in existing}
    items = list(existing)
    for text, hint, spell in extras:
        if text in seen:
            continue
        seen.add(text)
        items.append(item(text, hint, "phrase", spell))
    return write_items_pack(
        pack_id,
        title=title,
        lang=lang,
        description=description,
        version="1.1.0",
        items=items,
        source="curated-a1",
    )


def build_daily() -> list[dict]:
    books = []
    books.append(
        thicken_daily(
            "es-daily-a1-zh",
            ES_EXTRA_WORDS + ES_EXTRA_SENTS,
            title="西语日常 A1",
            lang="es",
            description="西班牙语入门词句 · 中文释义（加厚日常场景）",
        )
    )
    books.append(
        thicken_daily(
            "fr-daily-a1-zh",
            FR_EXTRA_WORDS + FR_EXTRA_SENTS,
            title="法语日常 A1",
            lang="fr",
            description="法语入门词句 · 中文释义（加厚日常场景，配合核心词表）",
        )
    )
    return books


def build_ja_n3() -> dict:
    rows = json.loads((CACHE / "kotoba-n3.json").read_text(encoding="utf-8"))
    items: list[dict] = []
    seen: set[str] = set()
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
        items.append(item(text, hint, "phrase", spell))
    return write_items_pack(
        "ja-jlpt-n3",
        title="日语 JLPT N3",
        lang="ja",
        description="JLPT N3 常用词 · 中文释义（罗马字拼写）",
        version="1.0.0",
        items=items,
        source="kotoba-jlpt",
    )


def hangul_to_romaja(text: str) -> str:
    from korean_romanizer.romanizer import Romanizer

    raw = Romanizer(text).romanize()
    return re.sub(r"\s+", " ", (raw or "").replace("-", "").strip().lower())


def build_yonsei(vol: int, pack_id: str, title: str) -> dict:
    payload = json.loads((CACHE / f"yonsei-vol{vol:02d}.json").read_text(encoding="utf-8"))
    rows = payload.get("rows") or []
    items: list[dict] = []
    seen: set[str] = set()
    for w in rows:
        if str(w.get("entry_kind") or "") == "grammar":
            continue
        text = (w.get("korean") or "").strip()
        hint = clean_hint(str(w.get("chinese") or ""))
        if not text or not hint or text in seen or len(text) > 24:
            continue
        try:
            spell = hangul_to_romaja(text)
        except Exception:
            spell = ""
        if not spell:
            continue
        seen.add(text)
        items.append(item(text, hint, "phrase", spell))
    return write_items_pack(
        pack_id,
        title=title,
        lang="ko",
        description=f"韩语进阶词 · 中文释义（《延世韩国语》第{vol}册开源词表）",
        version="1.0.0",
        items=items,
        source=f"open-yonsei-vol{vol}",
    )


_ART = re.compile(r"^(der|die|das|ein|eine)\s+", re.I)


def extract_zh_from_pos_meaning(pm: str) -> str:
    m = re.search(r"[\u4e00-\u9fff]", pm or "")
    if not m:
        return ""
    t = (pm or "")[m.start() :]
    t = re.split(r"[。；;\n]", t)[0]
    t = t.replace("„", "").replace("“", "").replace("”", "")
    t = re.sub(r"\s+", "", t)
    return clean_hint(t, max_len=40)


def load_de_zh_map() -> dict[str, str]:
    path = CACHE / "german_vocab.csv"
    out: dict[str, str] = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            word = (row.get("word") or "").strip()
            zh = extract_zh_from_pos_meaning(row.get("pos_meaning") or "")
            if word and zh:
                out.setdefault(word.casefold(), zh)
    return out


def de_lookup_keys(lemma: str) -> list[str]:
    lemma = lemma.strip()
    keys = [lemma.casefold()]
    bare = _ART.sub("", lemma).strip()
    if bare:
        keys.append(bare.casefold())
    if "/" in bare:
        for part in bare.split("/"):
            p = part.strip()
            if p:
                keys.append(p.casefold())
    # drop trailing punctuation / parentheses notes
    for k in list(keys):
        k2 = re.sub(r"\s*\(.*?\)\s*", "", k).strip()
        if k2 and k2 not in keys:
            keys.append(k2)
    return keys


# Small editorial fill for frequent A1 misses after article-stripped join.
DE_ZH_EXTRA = {
    "glücklich": "幸福的；高兴的",
    "anfangen": "开始",
    "fertig": "完成的；准备好的",
    "aufstehen": "起床；起立",
    "problem": "问题",
    "wetter": "天气",
    "gemüse": "蔬菜",
    "fieber": "发烧",
    "banane": "香蕉",
    "reise": "旅行",
    "wohnung": "公寓；住房",
    "wie viel": "多少",
    "was für ein": "什么样的",
    "circa": "大约",
    "ca.": "大约",
    "für": "为了；给",
    "ich": "我",
    "sich kümmern": "关心；照料",
    "zum beispiel": "例如",
    "zum beispiel/z. b.": "例如",
    "die großeltern (pl.)": "祖父母",
    "die pommes frites (pl.)": "薯条",
    "die lebensmittel (pl.)": "食品",
    "die papiere (pl.)": "证件；文件",
    "ihr/ihm/ihn": "她的/他（与格）/他（宾格）",
}


def _short_zh_gloss(zh: str, max_len: int = 28) -> str:
    t = (zh or "").strip()
    if not t:
        return ""
    t = re.split(r"[；;。\n]", t)[0].strip()
    if len(t) > max_len:
        t = t[:max_len].rstrip("，,、 ")
    return t


def build_de() -> dict:
    rows = json.loads((CACHE / "de-A1.json").read_text(encoding="utf-8"))
    zh_map = load_de_zh_map()
    for k, v in DE_ZH_EXTRA.items():
        zh_map.setdefault(k.casefold(), v)
    # Optional gap fill: lemma → ZH from EN definition bridge (cached).
    miss_fill_path = CACHE / "de_zh_miss_fill.json"
    if miss_fill_path.exists():
        raw_fill = json.loads(miss_fill_path.read_text(encoding="utf-8"))
        for lemma, zh in raw_fill.items():
            short = _short_zh_gloss(str(zh))
            if short:
                zh_map.setdefault(str(lemma).casefold(), short)

    lemmas: list[str] = []
    entries: list[dict] = []
    miss: list[str] = []
    seen: set[str] = set()
    for row in rows:
        lemma = str(row.get("lemma") or "").strip()
        if not lemma:
            continue
        key = lemma.casefold()
        if key in seen:
            continue
        zh = None
        for k in de_lookup_keys(lemma):
            if k in zh_map:
                zh = zh_map[k]
                break
        if not zh and key in zh_map:
            zh = zh_map[key]
        if not zh:
            miss.append(lemma)
            continue
        seen.add(key)
        lemmas.append(lemma)
        entry: dict = {
            "lemma": lemma,
            "display": lemma,
            "senses": [{"pos": str(row.get("pos") or "other"), "gloss": _short_zh_gloss(zh) or zh}],
        }
        if row.get("ipa"):
            entry["ipa"] = str(row["ipa"])
        entries.append(entry)
    print(f"  de A1: {len(lemmas)} hit, {len(miss)} miss")
    if miss[:20]:
        print("  miss sample:", ", ".join(miss[:20]))
    return write_lemma_pack(
        "de-core-a1-zh",
        title="德语 A1 核心",
        lang="de",
        description="德语入门核心词 · 中文释义（CEFR/Goethe A1）",
        version="1.0.1",
        lemmas=lemmas,
        entries=entries,
        source="cefr-de-a1+german-vocab-master",
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
    ap.add_argument("--only", default="daily,ja,ko,de")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    need = {x.strip() for x in args.only.split(",") if x.strip()}
    ensure_sources(args.refresh, need)
    built: list[dict] = []
    if "daily" in need:
        print("== fr/es daily ==")
        built.extend(build_daily())
    if "ja" in need:
        print("== ja-jlpt-n3 ==")
        built.append(build_ja_n3())
    if "ko" in need:
        print("== ko-yonsei-2/3 ==")
        built.append(build_yonsei(2, "ko-yonsei-2", "韩语延世 2"))
        built.append(build_yonsei(3, "ko-yonsei-3", "韩语延世 3"))
    if "de" in need:
        print("== de-core-a1-zh ==")
        built.append(build_de())
    update_catalog(built)
    for b in built:
        print(f"  {b['id']}: {b['lemmaCount']}")


if __name__ == "__main__":
    main()
