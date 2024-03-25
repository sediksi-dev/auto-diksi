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


# Module AI
## 1. Bot AGC
This module is used to generate an article based on the source article. This module has several modes which represent the flow of the article generation process. The modes are:
1. 'default': This mode is used to generate an article with this flow:
    - STEP 1: Extract the main points from the source article.
    - STEP 2: Generate an outline based on the created main points.
    - STEP 3: Generate the SEO data and writing guidelines using the created outline.
    - STEP 4: Create an introduction based on the outline, SEO data, and writing guidelines.
    - STEP 5: Loop through the outline and generate the content for each point. This process use the outline to inform the bot about the whole article structure, so the bot can generate the content for each point based on the writing guidelines, eventhough the bot only have the main points of the current section.
    - See the used prompt for each step >> [here](/helpers/prompts_library/bot_agc/default.md)
2. 'instant': _Coming soon_ (This mode is used to generate an article instantly without the need to create an outline first. This mode is suitable for generating an article with a short deadline.)
3. 'smart': _Coming soon_ (This mode is used to generate an article with a more complex structure. This mode is suitable for generating an article with a complex structure, such as a listicle article.)
4. _More modes will be added in the future. Are you have any idea for the new mode? Please let us know!_
