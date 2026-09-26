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
  <strong>Bahasa Indonesia</strong>
</p>

<p align="center"><strong>Installer desktop resmi dan sumber konten belajar.</strong></p>

<p align="center">
  <a href="#installer-desktop">Installer</a> ·
  <a href="#umpan-belajar">Umpan belajar</a> ·
  <a href="#katalog">Katalog</a> ·
  <a href="#lisensi">Lisensi</a> ·
  <a href="https://bubtype.com">Situs</a>
</p>

---

Repositori ini adalah **sumber distribusi dan konten resmi** BubType: installer desktop serta catalog buku kata / paket kalimat untuk dilanggan di aplikasi. Ikhtisar produk: [bubtype.com](https://bubtype.com).

Klien open-source: [BubType Community](https://github.com/ansurfen/bubtype-community).

## Installer desktop

Unduh dari [Releases](https://github.com/ansurfen/bubtype-packs/releases):

| Platform | Catatan |
| --- | --- |
| Windows | NSIS (`.exe`) |
| macOS | Ditandatangani & notarized (lihat nama aset Release) |

Installer adalah **build desktop komersial BubType**, hanya untuk dipasang pengguna akhir — **bukan** objek redistribusi Apache-2.0 untuk biner.

## Umpan belajar

Di BubType: **Temukan → Sumber langganan**, tambahkan:

```text
https://github.com/ansurfen/bubtype-packs/releases/latest/download/catalog.json
```

Gunakan **URL aset Release**. Saat rilis, taruh `catalog.json` dan semua `*-v1.json` di Assets yang sama.

## Katalog

| id | Catatan |
| --- | --- |
| `oxford-3000-{zh,en,ja}` | Oxford 3000 |
| `oxford-5000-{zh,en,ja}` | Oxford 5000 |
| `rant-*` | Kalimat orisinal BubType untuk latihan ketik |

## Struktur

| Path | Peran |
| --- | --- |
| `catalog.json` | Pintu feed |
| `*-v1.json` | Muatan paket |
| `docs/` | Dokumentasi multibahasa |
| `assets/` | Aset merek |
| Releases | Installer + catalog |

## Lisensi

| Konten | Ketentuan |
| --- | --- |
| Paket kalimat / catalog / dokumen BubType | [Apache License 2.0](../LICENSE) |
| Oxford 3000 / 5000 | Berdasar Oxford learner lists; **komersial: cek OUP** — di luar cakupan Apache repo ini |
| Installer Windows / macOS | **Proprietary** — hanya instalasi |

---

[bubtype.com](https://bubtype.com) · [Community](https://github.com/ansurfen/bubtype-community)
