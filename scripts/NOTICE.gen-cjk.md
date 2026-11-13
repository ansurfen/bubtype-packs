# Attribution for generated core packs

Packs produced by `scripts/gen_cjk_core_packs.py` / `scripts/build_zh_primary_packs.py`:

| Pack | Upstream | License |
| --- | --- | --- |
| `zh-hsk-1-3` | [HearMandarin HSK 3.0 word list](https://hearmandarin.com/datasets/) | CC BY 4.0 |
| `ja-jlpt-n5n4` | [SeupLio/kotoba-jlpt](https://github.com/SeupLio/kotoba-jlpt) processed N5+N4 (ZH glosses + romaji) | MIT |
| `ko-core-beginner` | [Open Yonsei Korean Vocabulary](https://github.com/Amulopapa67/open-yonsei-korean-vocabulary) vol.1 | CC BY-SA 3.0 |
| `es-core-a1-zh` | CEFR `es-A1` ([cefr-vocabulary-dataset](https://github.com/Talhakasikci/cefr-vocabulary-dataset)) × ZH map from [Learn_Spanish_w_Chinese](https://github.com/imabakagain/Learn_Spanish_w_Chinese) `spanish_vocab_8000_zh.csv` | upstream terms + packaging Apache-2.0 |

Chinese glosses come from the upstream bilingual datasets above (not machine-translated in this pipeline).

BubType packaging (manifest shape, catalog entries) is Apache-2.0 as per this repository.
Redistribute derivatives under the upstream licenses (especially ShareAlike for Yonsei).
