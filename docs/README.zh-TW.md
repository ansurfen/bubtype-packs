<p align="center">
  <img src="../assets/logo.png" width="96" alt="BubType logo" />
</p>

<h1 align="center">BubType Packs</h1>

<p align="center">
  <a href="./README.zh-CN.md">简体中文</a> ·
  <a href="./README.en.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="./README.ja.md">日本語</a> ·
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center"><strong>官方桌面安裝包與學習內容源。</strong></p>

<p align="center">
  <a href="#桌面安裝包">桌面安裝包</a> ·
  <a href="#學習內容訂閱">學習內容</a> ·
  <a href="#目前書單">書單</a> ·
  <a href="#授權">授權</a> ·
  <a href="https://bubtype.com">官網</a>
</p>

---

本倉庫是 BubType 的**官方發佈與內容源**：提供桌面安裝包，以及可在 App 內訂閱的詞書 / 句包 catalog。產品介紹見 [bubtype.com](https://bubtype.com)。

開源客戶端：[BubType Community](https://github.com/ansurfen/bubtype-community)。

## 桌面安裝包

至 [Releases](https://github.com/ansurfen/bubtype-packs/releases) 下載：

| 平台 | 說明 |
| --- | --- |
| Windows | NSIS 安裝包（`.exe`） |
| macOS | 已簽名公證的安裝包（以 Release 資源為準） |

安裝包為 **BubType 商業桌面建置**，僅授權最終使用者安裝，**不適用** Apache-2.0 對二進位再發佈的條款。

## 學習內容訂閱

在 BubType「探索 → 訂閱源」加入：

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

請使用 **Release 資源網址**。發佈時請將 `catalog.json` 與各 `*-v1.json` 放在同一 Release Assets。

## 目前書單

| id | 說明 |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000（釋義語言分軌） |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 |
| `rant-workplace` | 職場吐槽 |
| `rant-campus` | 校園吐槽 |
| `rant-invest` | 投資吐槽 |
| `rant-ecommerce` | 電商人吐槽 |

吐槽系列為 **BubType 原創例句**，非抓取社群貼文。

## 倉庫結構

| 路徑 | 用途 |
| --- | --- |
| `catalog.json` | 書單入口 |
| `*-v1.json` | 詞書 / 句包 |
| `docs/` | 多語說明 |
| `assets/` | 品牌資源 |
| Releases | 安裝包與 catalog |

## 授權

| 內容 | 條款 |
| --- | --- |
| BubType 原創句包、catalog 與文件 | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 | 基於 Oxford learner word lists；**商用請自行核對 OUP 條款**，不在本倉 Apache 範圍 |
| Windows / macOS 安裝包 | **專有**：僅授權安裝，禁止擅自再發佈 |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
