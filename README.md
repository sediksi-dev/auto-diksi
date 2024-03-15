Sebelum membuild ke portainer, pastikan bahwa package `websockets` yang terdapat pada `requirements.txt` adalah versi 11.0.3.

Step by Step untuk melakukan compose ke portainer:
1. Buka portainer pada browser (portainer.likrea.biz.id)
2. Login menggunakan akun yang telah terdaftar
3. Hapus stack yang sudah ada (jika ada)
4. Pastikan bahwa image yang akan di deploy sudah dihapus.
5. Pilih `Stacks` pada sidebar
6. Klik `Add stack`
7. Isi `Name` dengan nama stack yang diinginkan
8. Pilih sumber berupa Git Repository
9. Isi `Git Repository URL` dengan `https://github.com/sediksi-dev/auto-diksi`
10. Isi `Compose file path` dengan `docker-compose.yml`
11. Centang `Authentication` dan isi `Username` dan `Password` dengan username dan password yang telah terdaftar
12. Pada kolom password, masukkan `Personal Access Token` yang telah dibuat pada repository
13. `Personal Access Token` dapat dibuat pada `Settings` -> `Developer settings` -> `Personal access tokens` -> `Generate new token` di github
14. Klik `Deploy the stack`
