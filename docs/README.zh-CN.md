<p align="center">
  <img src="../assets/logo.png" width="96" alt="BubType logo" />
</p>

<h1 align="center">BubType Packs</h1>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="./README.en.md">English</a> ·
  <a href="./README.zh-TW.md">繁體中文</a> ·
  <a href="./README.ja.md">日本語</a> ·
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center"><strong>官方桌面安装包与学习内容源。</strong></p>

<p align="center">
  <a href="#桌面安装包">桌面安装包</a> ·
  <a href="#学习内容订阅">学习内容</a> ·
  <a href="#当前书单">书单</a> ·
  <a href="#许可">许可</a> ·
  <a href="https://bubtype.com">官网</a>
</p>

---

本仓库是 BubType 的**官方分发与内容源**：发布桌面安装包，并提供可在 App 内订阅的词书 / 句包 catalog。产品介绍与 Pro 能力见 [bubtype.com](https://bubtype.com)。

开源客户端源码见 [BubType Community](https://github.com/ansurfen/bubtype-community)。

## 桌面安装包

在 [Releases](https://github.com/ansurfen/bubtype-packs/releases) 下载适用于你系统的安装包：

| 平台 | 说明 |
| --- | --- |
| Windows | NSIS 安装包（`.exe`） |
| macOS | 已签名公证的安装包（`.dmg` 等，以 Release 资源名为准） |

安装包为 **BubType 商业桌面构建**，版权归 BubType，仅授权最终用户安装使用，**不适用** Apache-2.0 对二进制的再分发条款。获取与功能说明以官网为准。

## 学习内容订阅

在 BubType「发现 → 订阅源」添加：

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

请使用 **Release 资源地址**（如上）。开发调试才可临时使用仓库 raw，不推荐作为日常订阅。

发布新版本时：将 `catalog.json` 与各 `*-v1.json` **放在同一 Release 的 Assets 中**。若 `catalog.json` 里的 `asset` 为相对路径，客户端会相对 **catalog 所在目录** 解析。

## 当前书单

| id | 说明 |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000 核心词（释义语言分轨） |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 拓展词 |
| `rant-workplace` | 职场吐槽 · 英文短句 / 中文提示 |
| `rant-campus` | 校园吐槽 |
| `rant-invest` | 投资吐槽 |
| `rant-ecommerce` | 电商人吐槽 |

吐槽系列为 **BubType 原创例句**（可用于跟打练习），并非抓取社交媒体。

## 仓库结构

| 路径 | 用途 |
| --- | --- |
| `catalog.json` | 书单入口 |
| `*-v1.json` | 词书 / 句包数据 |
| `docs/` | 多语言说明（本目录） |
| `assets/` | 品牌资源（如 logo） |
| Releases | 安装包与 catalog 发布物 |

## 许可

| 内容 | 许可 |
| --- | --- |
| BubType 原创句包、catalog 结构与本仓库文档 | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 词表整理 | 基于 Oxford learner word lists；释义与配套整理供学习使用。**商用请自行核对 Oxford / OUP 条款**，不在本仓 Apache 授权范围内 |
| Windows / macOS 安装包 | **专有软件**：仅授权安装使用，禁止擅自再分发或二次打包 |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
