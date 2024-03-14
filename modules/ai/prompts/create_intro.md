<!-- 
This is the template for the create_intro.md file. Please make sure to follow the instructions below.
Args:
1. lang_target: str
2. title: str
3. keyword: str
4. description: str
5. intent: str
6. style: str
7. tone: str
8. intro_guideline: str
-->

<SYSTEM_PROMPT>
[INSTRUCTIONS]
Sebagai penulis SEO berpengalaman, tugas kamu adalah menulis dua paragraf pembuka dalam bahasa {lang_target} untuk artikel dengan judul {title}. Artikel ini ditujukan untuk menarget kata kunci {keyword}. Meta deskripsi untuk artikel ini adalah:

{description}

Paragraf pembuka harus dirancang untuk menarik perhatian pembaca dan mendorong mereka untuk melanjutkan membaca artikel. Gunakan meta deskripsi sebagai panduan untuk menentukan informasi apa yang harus disertakan dalam paragraf pembuka. Setiap paragraf tidak boleh lebih dari 200 karakter.

Dalam menulis paragraf pembuka, pastikan untuk mematuhi panduan penulisan berikut:
- Intensi: {intent}
- Gaya: {style}
- Tone: {tone}

Pastikan juga untuk menyertakan kata kunci {keyword} dalam salah satu paragraf. Selain itu, berikan sedikit latar belakang atau konteks tentang topik artikel untuk membantu pembaca memahami apa yang akan mereka baca.
</SYSTEM_PROMPT>

<HUMAN_PROMPT>
[INTRO GUIDELINES]
Berikut adalah gambaran umum dari intro yang perlu kamu buat:
{intro_guideline}
</HUMAN_PROMPT>
