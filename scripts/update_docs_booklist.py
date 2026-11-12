# -*- coding: utf-8 -*-
from pathlib import Path

docs = Path(__file__).resolve().parents[1] / "docs"

zh_cn = docs / "README.zh-CN.md"
en = docs / "README.en.md"

zh_text = zh_cn.read_text(encoding="utf-8")
if "`fr-daily-a1-zh`" not in zh_text:
    old = """| `fr-core-a1-zh` | 法语 A1 核心 |

吐槽系列为 **BubType 原创例句**（可用于跟打练习），并非抓取社交媒体。法语包的 `lang` 为 `fr`，可在发现页按练习语言筛选。"""
    new = """| `fr-core-a1-zh` | 法语 A1 核心 |
| `fr-daily-a1-zh` | 法语日常 A1（词+句） |
| `zh-daily-a1` | 中文日常 A1（词+句 / 拼音） |
| `ja-daily-a1` | 日语日常 A1（词+句 / 罗马字） |
| `ko-daily-a1-zh` | 韩语日常 A1（词+句 / 罗马音） |
| `es-daily-a1-zh` | 西语日常 A1（词+句） |

吐槽系列为 **BubType 原创例句**（可用于跟打练习），并非抓取社交媒体。多语日常包带 `spell` 字段，可在原文 / 拼写模式间切换；可按练习语言筛选。"""
    if old in zh_text:
        zh_cn.write_text(zh_text.replace(old, new), encoding="utf-8")
        print("zh-CN replaced")
    elif "| `fr-core-a1-zh`" not in zh_text:
        # insert after rant-ecommerce
        lines = zh_text.splitlines()
        out = []
        for line in lines:
            out.append(line)
            if line.startswith("| `rant-ecommerce`"):
                out.extend(
                    [
                        "| `fr-core-a1-zh` | 法语 A1 核心 |",
                        "| `fr-daily-a1-zh` | 法语日常 A1（词+句） |",
                        "| `zh-daily-a1` | 中文日常 A1（词+句 / 拼音） |",
                        "| `ja-daily-a1` | 日语日常 A1（词+句 / 罗马字） |",
                        "| `ko-daily-a1-zh` | 韩语日常 A1（词+句 / 罗马音） |",
                        "| `es-daily-a1-zh` | 西语日常 A1（词+句） |",
                    ]
                )
        zh_cn.write_text("\n".join(out) + ("\n" if zh_text.endswith("\n") else ""), encoding="utf-8")
        print("zh-CN inserted from ecommerce")
    else:
        raise SystemExit("zh-CN unexpected")
else:
    print("zh-CN already ok")

en_text = en.read_text(encoding="utf-8")
if "`fr-daily-a1-zh`" not in en_text:
    old = """| `fr-core-a1-zh` | French A1 core |

Rant packs are **BubType original sentences** for typing practice — not scraped social posts. French packs use `lang: \"fr\"` and can be filtered on Discover by practice language."""
    new = """| `fr-core-a1-zh` | French A1 core |
| `fr-daily-a1-zh` | French A1 daily (words + sentences) |
| `zh-daily-a1` | Chinese A1 daily (words + sentences / pinyin) |
| `ja-daily-a1` | Japanese A1 daily (words + sentences / romaji) |
| `ko-daily-a1-zh` | Korean A1 daily (words + sentences / romaja) |
| `es-daily-a1-zh` | Spanish A1 daily (words + sentences) |

Rant packs are **BubType original sentences** for typing practice — not scraped social posts. Multilingual daily packs include a `spell` field for script/spell practice and can be filtered by practice language on Discover."""
    if old in en_text:
        en.write_text(en_text.replace(old, new), encoding="utf-8")
        print("en replaced")
    else:
        raise SystemExit("en unexpected")
else:
    print("en already ok")

extras = {
    "README.zh-TW.md": [
        "| `fr-core-a1-zh` | 法語 A1 核心 |",
        "| `fr-daily-a1-zh` | 法語日常 A1（詞+句） |",
        "| `zh-daily-a1` | 中文日常 A1（詞+句 / 拼音） |",
        "| `ja-daily-a1` | 日語日常 A1（詞+句 / 羅馬字） |",
        "| `ko-daily-a1-zh` | 韓語日常 A1（詞+句 / 羅馬音） |",
        "| `es-daily-a1-zh` | 西語日常 A1（詞+句） |",
    ],
    "README.ja.md": [
        "| `fr-core-a1-zh` | フランス語 A1 コア |",
        "| `fr-daily-a1-zh` | フランス語 A1 日常（語＋文） |",
        "| `zh-daily-a1` | 中国語 A1 日常（語＋文 / 拼音） |",
        "| `ja-daily-a1` | 日本語 A1 日常（語＋文 / ローマ字） |",
        "| `ko-daily-a1-zh` | 韓国語 A1 日常（語＋文 / ローマ字） |",
        "| `es-daily-a1-zh` | スペイン語 A1 日常（語＋文） |",
    ],
    "README.vi.md": [
        "| `fr-core-a1-zh` | Tiếng Pháp A1 cốt lõi |",
        "| `fr-daily-a1-zh` | Tiếng Pháp A1 hàng ngày |",
        "| `zh-daily-a1` | Tiếng Trung A1 hàng ngày |",
        "| `ja-daily-a1` | Tiếng Nhật A1 hàng ngày |",
        "| `ko-daily-a1-zh` | Tiếng Hàn A1 hàng ngày |",
        "| `es-daily-a1-zh` | Tiếng Tây Ban Nha A1 hàng ngày |",
    ],
    "README.id.md": [
        "| `fr-core-a1-zh` | Prancis A1 inti |",
        "| `fr-daily-a1-zh` | Prancis A1 harian |",
        "| `zh-daily-a1` | Mandarin A1 harian |",
        "| `ja-daily-a1` | Jepang A1 harian |",
        "| `ko-daily-a1-zh` | Korea A1 harian |",
        "| `es-daily-a1-zh` | Spanyol A1 harian |",
    ],
}

for name, rows in extras.items():
    p = docs / name
    text = p.read_text(encoding="utf-8")
    if "`fr-daily-a1-zh`" in text:
        print(name, "already ok")
        continue
    lines = text.splitlines()
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if (not inserted) and line.startswith("| `rant-ecommerce`"):
            # drop existing fr-core if present on next lines handled by only inserting once
            out.extend(rows)
            inserted = True
    if not inserted:
        raise SystemExit(f"{name}: no rant-ecommerce row")
    # remove duplicate fr-core if we just added a set that includes it and old fr-core remains
    cleaned = []
    seen_ids = set()
    for line in out:
        if line.startswith("| `") and " |" in line:
            pid = line.split("`")[1]
            if pid in seen_ids and pid.startswith(("fr-", "zh-", "ja-", "ko-", "es-")):
                continue
            if pid.startswith(("oxford-", "rant-", "fr-", "zh-", "ja-", "ko-", "es-")):
                seen_ids.add(pid)
        cleaned.append(line)
    p.write_text("\n".join(cleaned) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print(name, "updated")
