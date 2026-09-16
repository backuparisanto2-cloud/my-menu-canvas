# Menu Kantin Inyong — Katalog Menu Mobile-First

Halaman menu satu-halaman: 9 gambar menu, satu gambar per "halaman", scroll ke bawah, ringan dan cepat.

## Tampilan

- Tanpa header. Satu tombol menu melayang (kiri atas) membuka sidebar berisi daftar halaman.
- Di mobile setiap gambar tampil hampir memenuhi layar; di layar lebar gambar dibatasi lebarnya dan ditengahkan.
- Latar mengikuti warna poster (krem hangat, aksen hijau dan cokelat dari logo Umaeh Inyong).
- Efek fade-in halus saat gambar masuk layar (IntersectionObserver + transisi CSS, bukan library animasi).
- Tombol "kembali ke atas" muncul setelah pengguna menggulir jauh, dengan scroll halus.

## Daftar halaman (urutan)

1. Sampul — Umaeh Inyong (jam buka & alamat)
2. Menu Kalibul — Sate Inyong, Paket 5 Sate, Nasi Goreng Kambing
3. Menu Kalibul — Gule, Tongseng, Sop Kambing, Kalibuling, Kambing Gongso
4. Sate Kambing se Dunia — Bulgogi, Teriyaki, Cheese, Shaslik
5. Sate Kambing se Dunia — Mentega, Lada Hitam, Barbeque, Curry
6. Legenda — nasi rames, nasi goreng, ayam
7. Legenda — gado-gado, mendoan gejot, kupat tahu, bakmi jawa, nasi pecel, lontong opor
8. Bandeng Pepes Inyong & oseng
9. Smart Rice — semua varian Rp 10.000

Judul tiap halaman dipakai untuk penamaan di sidebar; bisa diubah nanti.

## Favorit

- Ikon bintang di tiap halaman untuk menandai favorit.
- Halaman favorit ditandai juga di sidebar, dengan filter "tampilkan favorit saja".
- Tanda favorit hilang saat halaman di-refresh (disimpan hanya selama sesi di memori).

## Gambar & kecepatan

- Semua foto dikonversi ke WebP, target maksimal 50KB per file dengan kualitas tetap terbaca (lebar dibatasi, kualitas dicari otomatis sampai di bawah 50KB).
- Gambar pertama dimuat prioritas; sisanya lazy-load dengan ukuran ruang tetap agar tidak "lompat".
- Tanpa font eksternal berat, tanpa library animasi tambahan.

## Ekspor HTML

- Tombol "Unduh HTML" pada sidebar menghasilkan satu berkas HTML statis berisi seluruh halaman menu dengan gambar tertanam, bisa dibuka offline tanpa server.

## Catatan teknis

- Halaman dibangun di `src/routes/index.tsx` dengan komponen `MenuPage` dan `MenuSidebar` (Sheet shadcn).
- Gambar dikompres via `sharp` di sandbox, hasil `.webp` diunggah lewat `lovable-assets`, pointer `.asset.json` disimpan di `src/assets/menu/`.
- Daftar halaman didefinisikan sebagai array indeks gambar di `src/data/menu-pages.ts`, dipakai bersama oleh konten, sidebar, dan ekspor HTML.
- Favorit: React state di komponen induk (bukan localStorage), sehingga hilang saat refresh.
- Ekspor: fungsi klien yang merangkai string HTML + CSS inline dan URL gambar CDN, lalu diunduh sebagai Blob.
- SEO: `head()` pada route index dengan judul dan deskripsi Kantin Inyong.
