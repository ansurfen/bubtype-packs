# bubtype-wordbooks

BubType 官方词书订阅源（catalog + packs）。

## 订阅地址

发布 Release 后，在 BubType「发现 → 订阅源」添加：

```text
https://github.com/ansurfen/bubtype-wordbooks/releases/latest/download/catalog.json
```

开发时也可直接用 raw（不推荐生产）：

```text
https://raw.githubusercontent.com/ansurfen/bubtype-wordbooks/main/catalog.json
```

> `catalog.json` 里的 `asset` 若是相对路径，客户端会相对 **catalog 所在目录** 解析。  
> 用 Release 时，请把 `catalog.json` 与各 `*-v1.json` **放在同一个 Release 资源列表里**。

## 当前书单

| id | 说明 |
|---|---|
| `oxford-3000-{zh,en,ja}` | Oxford 3000 核心词（释义语言分轨） |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 拓展词 |
| `rant-workplace` | 职场吐槽 · 英文短句 / 中文提示 |
| `rant-campus` | 校园吐槽 |
| `rant-invest` | 投资吐槽 |
| `rant-ecommerce` | 电商人吐槽 |

吐槽系列为 **BubType 原创例句**（可打字练习），不是抓取社交媒体。

## 格式

- `catalog.json`：书单清单（Clash 式订阅入口）
- `*-v1.json`：词书包（`manifest` + `items` 句子，或 Oxford 的 `lemmas`/`entries`）

## License

- 吐槽句包：BubType original content
- Oxford 词表：基于 Oxford 3000 / 5000 learner word lists；释义与例句整理自学习用途资源，若商用请自行核对 OUP 条款
