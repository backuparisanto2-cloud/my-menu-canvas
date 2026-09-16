# Menu lebih ringan + tombol bagikan WhatsApp

## 1. Gambar lebih kecil (maks 30 KB)

- Semua 9 gambar dikompres ulang ke WebP dengan target maksimal 30 KB per gambar
  (sekarang batasnya 50 KB), lebar disesuaikan agar tulisan poster tetap terbaca.
- Kualitas diuji satu per satu: turunkan kualitas bertahap sampai di bawah 30 KB,
  lalu dicek hasilnya secara visual sebelum dipakai.
- Gambar lama diganti dengan yang baru, alamat gambar di dalam aplikasi ikut
  diperbarui, termasuk pada berkas HTML yang bisa diunduh.

## 2. Loading lebih cepat

- Hanya gambar pertama yang dimuat lebih awal; sisanya dimuat sedikit lebih
  dekat ke layar agar pemakaian data awal turun.
- Ruang tiap gambar tetap dipesan lebih dulu supaya halaman tidak melompat.
- Gambar yang jauh dari layar dilepas dari proses gambar ulang browser
  (hemat memori di ponsel lama).

## 3. Tombol bagikan WhatsApp di kiri atas gambar

- Tombol bulat hijau dengan ikon WhatsApp di pojok kiri atas tiap gambar
  (berpasangan dengan bintang favorit di kanan atas), juga tersedia di
  tampilan layar penuh.
- Saat ditekan: gambar tersebut dikirim sebagai berkas lewat menu berbagi
  ponsel, jadi bisa langsung dipilih WhatsApp dan dikirim ke teman/grup.
- Bila ponsel atau browser tidak mendukung kirim berkas, otomatis beralih ke
  WhatsApp dengan pesan berisi nama menu dan tautan gambarnya.
- Di komputer, tombol membuka WhatsApp Web dengan tautan gambar.

## Catatan teknis

- Kompresi ulang dengan PIL (LANCZOS, method 6, cari kualitas tertinggi yang
  masih < 30 KB), unggah via `lovable-assets`, pointer di `src/assets/menu/`.
- `shareMenuImage(page)` baru di `src/lib/share-menu.ts`: `fetch(url)` → `Blob`
  → `File` → `navigator.canShare({ files })` → `navigator.share`; fallback
  `https://wa.me/?text=<judul + URL absolut gambar>`.
- Tombol ditambahkan di `MenuFigure` (`src/routes/index.tsx`) dan bar atas
  `MenuLightbox`; HTML ekspor (`src/lib/export-menu-html.ts`) mendapat versi
  JS inline yang sama, tetap tanpa pustaka luar.
- Verifikasi: cek ukuran berkas semua gambar < 30 KB, tsgo bersih, uji Playwright
  390x844 (tombol tampil, fallback WhatsApp terpanggil, tanpa error konsol).
