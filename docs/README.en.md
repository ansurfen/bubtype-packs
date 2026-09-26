<p align="center">
  <img src="../assets/logo.png" width="96" alt="BubType logo" />
</p>

<h1 align="center">BubType Packs</h1>

<p align="center">
  <a href="./README.zh-CN.md">简体中文</a> ·
  <a href="./README.en.md">English</a> ·
  <a href="./README.zh-TW.md">繁體中文</a> ·
  <a href="./README.ja.md">日本語</a> ·
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center"><strong>Official desktop installers and learning content feeds.</strong></p>

<p align="center">
  <a href="#desktop-installers">Installers</a> ·
  <a href="#learning-feeds">Learning feeds</a> ·
  <a href="#catalog">Catalog</a> ·
  <a href="#license">License</a> ·
  <a href="https://bubtype.com">Website</a>
</p>

---

This repository is BubType’s **official distribution and content source**: desktop installers, plus wordbook / sentence-pack catalogs you can subscribe to in the app. Product overview: [bubtype.com](https://bubtype.com).

Open-source client sources: [BubType Community](https://github.com/ansurfen/bubtype-community).

## Desktop installers

Download builds for your platform from [Releases](https://github.com/ansurfen/bubtype-packs/releases):

| Platform | Notes |
| --- | --- |
| Windows | NSIS installer (`.exe`) |
| macOS | Signed & notarized packages (see Release asset names) |

Installers are **BubType commercial desktop builds**. Copyright BubType. Licensed for end-user installation only — **not** covered by Apache-2.0 redistribution terms for binaries. See the website for product details.

## Learning feeds

In BubType, open **Discover → Subscriptions** and add:

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

Prefer the **Release asset URL** above. Raw GitHub URLs are for local debugging only.

When publishing: put `catalog.json` and every `*-v1.json` in the **same Release Assets** list. Relative `asset` paths resolve against the catalog’s directory.

## Catalog

| id | Notes |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000 (gloss language tracks) |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 |
| `rant-workplace` | Workplace rants · EN lines / ZH hints |
| `rant-campus` | Campus rants |
| `rant-invest` | Investing rants |
| `rant-ecommerce` | E-commerce rants |

Rant packs are **BubType original sentences** for typing practice — not scraped social posts.

## Layout

| Path | Role |
| --- | --- |
| `catalog.json` | Feed entry |
| `*-v1.json` | Pack payloads |
| `docs/` | Localized docs (this folder) |
| `assets/` | Brand assets |
| Releases | Installers + published catalog |

## License

| Content | Terms |
| --- | --- |
| BubType-authored packs, catalog schema, docs | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 lists | Based on Oxford learner word lists; curated for study. **Commercial use: check Oxford / OUP terms.** Not under this repo’s Apache grant |
| Windows / macOS installers | **Proprietary** — install-only; no redistribution or repackaging |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
