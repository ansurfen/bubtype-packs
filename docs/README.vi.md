<p align="center">
  <img src="../assets/logo.png" width="96" alt="BubType logo" />
</p>

<h1 align="center">BubType Packs</h1>

<p align="center">
  <a href="./README.zh-CN.md">简体中文</a> ·
  <a href="./README.en.md">English</a> ·
  <a href="./README.zh-TW.md">繁體中文</a> ·
  <a href="./README.ja.md">日本語</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center"><strong>Bản cài desktop chính thức và nguồn nội dung học.</strong></p>

<p align="center">
  <a href="#cai-dat-desktop">Cài đặt</a> ·
  <a href="#nguon-hoc">Nguồn học</a> ·
  <a href="#danh-muc">Danh mục</a> ·
  <a href="#giay-phep">Giấy phép</a> ·
  <a href="https://bubtype.com">Website</a>
</p>

---

Kho này là **kênh phân phối và nội dung chính thức** của BubType: bản cài desktop và catalog từ sách / gói câu để đăng ký trong app. Giới thiệu sản phẩm: [bubtype.com](https://bubtype.com).

Client mã nguồn mở: [BubType Community](https://github.com/ansurfen/bubtype-community).

## Cài đặt desktop

Tải từ [Releases](https://github.com/ansurfen/bubtype-packs/releases):

| Nền tảng | Ghi chú |
| --- | --- |
| Windows | NSIS (`.exe`) |
| macOS | Đã ký & notarize (xem tên file trên Release) |

Bản cài là **build desktop thương mại BubType**, chỉ được phép cài đặt — **không** thuộc điều khoản tái phân phối Apache-2.0 cho binary.

## Nguồn học

Trong BubType: **Khám phá → Nguồn đăng ký**, thêm:

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

Dùng **URL asset trên Release**. Khi phát hành, đặt `catalog.json` và các `*-v1.json` trong cùng Assets.

## Danh mục

| id | Ghi chú |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000 |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 |
| `rant-*` | Câu gốc BubType để luyện gõ |

## Cấu trúc

| Đường dẫn | Vai trò |
| --- | --- |
| `catalog.json` | Lối vào feed |
| `*-v1.json` | Gói dữ liệu |
| `docs/` | Tài liệu đa ngôn ngữ |
| `assets/` | Thương hiệu |
| Releases | Bản cài + catalog |

## Giấy phép

| Nội dung | Điều khoản |
| --- | --- |
| Gói câu / catalog / tài liệu BubType | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 | Theo Oxford learner lists; **thương mại: kiểm tra OUP** — ngoài phạm vi Apache của kho này |
| Bản cài Windows / macOS | **Độc quyền** — chỉ cài đặt |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
