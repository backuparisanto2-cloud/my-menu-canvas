# Optimasi Mobile: Favorit Tersimpan, Fullscreen & Zoom, Animasi Antar Gambar

## Yang akan dibuat

### 1. Favorit tersimpan 60 menit
- Bintang favorit disimpan di penyimpanan lokal perangkat, jadi tidak hilang saat halaman di-refresh.
- Setiap favorit punya masa berlaku 60 menit sejak terakhir ditandai; setelah lewat, tanda bintang otomatis hilang.
- Saat halaman dibuka, favorit kedaluwarsa dibersihkan lebih dulu; ada juga pemeriksaan berkala tiap menit agar bintang hilang sendiri tanpa perlu refresh.

### 2. Satu gambar tampil penuh layar (khusus mobile)
- Ketuk sekali pada gambar membuka tampilan layar penuh dengan latar gelap.
- Di layar penuh: geser kiri/kanan untuk pindah gambar, tombol tutup, nomor halaman (mis. "3 / 9"), dan tombol bintang favorit.
- Tombol perangkat "kembali" menutup tampilan penuh, bukan meninggalkan halaman.
- Halaman di belakang terkunci agar tidak ikut bergulir.

### 3. Ketuk dua kali untuk perbesar
- Di tampilan layar penuh, ketuk dua kali memperbesar gambar sekitar 2,5x tepat di titik yang disentuh; ketuk dua kali lagi kembali normal.
- Saat diperbesar bisa digeser untuk melihat bagian lain, dan cubit dua jari juga bekerja.
- Saat diperbesar, geser antar gambar dinonaktifkan agar tidak bentrok.

### 4. Animasi antar gambar yang elegan tapi ringan
- Gambar muncul dengan gerakan halus: naik sedikit, memudar masuk, disertai sedikit pembesaran dan kemiringan lembut — hanya memakai transformasi ringan yang ditangani kartu grafis.
- Setiap gambar diberi jeda sangat kecil agar terasa berurutan dan mewah.
- Perpindahan di layar penuh memakai transisi geser-memudar.
- Bila perangkat diatur "kurangi gerakan", semua animasi dimatikan otomatis.

### 5. Optimasi kecepatan mobile
- Dua gambar pertama dimuat lebih awal, sisanya dimuat saat mendekati layar.
- Ruang gambar dipesan lebih dulu sehingga halaman tidak "melompat" saat memuat.
- Berkas HTML hasil unduhan ikut diperbarui: fullscreen, ketuk-dua-kali untuk zoom, favorit 60 menit, dan animasi yang sama — tetap tanpa pustaka tambahan.

## Catatan teknis

- `src/hooks/use-favorites.ts` (baru): state favorit berupa peta `id -> timestamp`, disimpan di `localStorage` kunci `inyong-fav-v1`, TTL 60 menit, pembersihan saat mount + interval 60 detik, ditulis hanya di `useEffect` agar aman untuk SSR/hidrasi.
- `src/components/menu-lightbox.tsx` (baru): overlay `position: fixed`, Pointer Events untuk swipe dan pinch, transform `translate/scale` dengan `transform-origin: 0 0`, anchor zoom pada titik ketuk, deteksi double-tap via jeda < 300 ms, `touch-action: none`, `history.pushState` untuk tombol back.
- `src/routes/index.tsx`: memakai hook favorit dan lightbox; `MenuFigure` menambah `style={{ transitionDelay }}`, `will-change: transform, opacity`, `contain: content`, serta `aspect-ratio` dari `IMAGE_WIDTH/IMAGE_HEIGHT`.
- `src/lib/export-menu-html.ts`: CSS/JS inline diperluas dengan lightbox, double-tap zoom, `localStorage` favorit ber-TTL, dan animasi bertahap; tetap satu berkas tanpa dependensi.
- Semua animasi memakai `opacity` + `transform` saja; `prefers-reduced-motion` dihormati di aplikasi dan di berkas ekspor.
