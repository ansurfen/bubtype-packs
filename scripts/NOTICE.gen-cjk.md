# Attribution for generated core packs

Packs produced by `scripts/gen_cjk_core_packs.py` / `scripts/build_zh_primary_packs.py` / `scripts/expand_p1_packs.py`:

| Pack | Upstream | License |
| --- | --- | --- |
| `zh-hsk-1-3` | [HearMandarin HSK 3.0 word list](https://hearmandarin.com/datasets/) | CC BY 4.0 |
| `ja-jlpt-n5n4` / `ja-jlpt-n3` | [SeupLio/kotoba-jlpt](https://github.com/SeupLio/kotoba-jlpt) processed N5–N3 (ZH + romaji) | MIT |
| `ko-core-beginner` / `ko-yonsei-2` / `ko-yonsei-3` | [Open Yonsei Korean Vocabulary](https://github.com/Amulopapa67/open-yonsei-korean-vocabulary) vols 1–3 | CC BY-SA 3.0 |
| `es-core-a1-zh` | CEFR `es-A1` ([cefr-vocabulary-dataset](https://github.com/Talhakasikci/cefr-vocabulary-dataset)) × ZH map from [Learn_Spanish_w_Chinese](https://github.com/imabakagain/Learn_Spanish_w_Chinese) | upstream + Apache-2.0 packaging |
| `de-core-a1-zh` | CEFR/Goethe `de-A1` × [German-Vocabulary-Master](https://github.com/ShaoWanqiu/German-Vocabulary-Master) DE–ZH CSV; remaining gaps bridged from English `definition_target` | upstream + Apache-2.0 packaging |
| `fr-daily-a1-zh` / `es-daily-a1-zh` | Curated A1 daily scenes (BubType) | Apache-2.0 |

Chinese glosses come from the upstream bilingual datasets above (not bulk machine-translated), except small editorial fills and DE A1 gap-bridge noted in `expand_p1_packs.py`.

BubType packaging (manifest shape, catalog entries) is Apache-2.0 as per this repository.
Redistribute derivatives under the upstream licenses (especially ShareAlike for Yonsei).
