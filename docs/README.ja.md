<p align="center">
  <img src="../assets/logo.png" width="96" alt="BubType logo" />
</p>

<h1 align="center">BubType Packs</h1>

<p align="center">
  <a href="./README.zh-CN.md">简体中文</a> ·
  <a href="./README.en.md">English</a> ·
  <a href="./README.zh-TW.md">繁體中文</a> ·
  <strong>日本語</strong> ·
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center"><strong>公式デスクトップ版インストーラと学習コンテンツ配信。</strong></p>

<p align="center">
  <a href="#デスクトップ版">インストーラ</a> ·
  <a href="#学習フィード">学習フィード</a> ·
  <a href="#カタログ">カタログ</a> ·
  <a href="#ライセンス">ライセンス</a> ·
  <a href="https://bubtype.com">サイト</a>
</p>

---

このリポジトリは BubType の**公式配布・コンテンツ源**です。デスクトップ版インストーラと、アプリ内で購読できる単語帳 / 文パックの catalog を公開します。製品概要は [bubtype.com](https://bubtype.com)。

OSS クライアント：[BubType Community](https://github.com/ansurfen/bubtype-community)。

## デスクトップ版

[Releases](https://github.com/ansurfen/bubtype-packs/releases) からダウンロード：

| 平台 | 内容 |
| --- | --- |
| Windows | NSIS（`.exe`） |
| macOS | 署名・公証済み（Release のファイル名を確認） |

インストーラは **BubType 商用デスクトップビルド**です。エンドユーザーのインストールのみ許可。バイナリの再配布は Apache-2.0 の対象外です。

## 学習フィード

アプリの「発見 → 購読ソース」に追加：

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

**Release のアセット URL** を使ってください。公開時は `catalog.json` と各 `*-v1.json` を同じ Release に置きます。

## カタログ

| id | 内容 |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000（訳語トラック） |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 |
| `rant-workplace` / `campus` / `invest` / `ecommerce` | BubType オリジナル短文 |

## 構成

| パス | 役割 |
| --- | --- |
| `catalog.json` | フィード入口 |
| `*-v1.json` | パック本体 |
| `docs/` | 多言語ドキュメント |
| `assets/` | ブランド資産 |
| Releases | インストーラと catalog |

## ライセンス

| 内容 | 条件 |
| --- | --- |
| BubType オリジナル文・catalog・文書 | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 | Oxford learner lists に基づく。**商用は OUP 条項を確認**。本リポの Apache 範囲外 |
| インストーラ | **プロプライエタリ** — インストールのみ |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
