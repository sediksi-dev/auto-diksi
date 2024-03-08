from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# from helper.md_prompt import prompt_from_md

# from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def extract_info(content: str):
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", verbose=True)

    facts_prompt = ChatPromptTemplate.from_template(
        """Tolong analisis dan ekstrak semua informasi dan fakta penting dari konten yang diberikan dalam bahasa {language}. Pastikan setiap detail, tidak peduli seberapa kecil, dicatat dan tidak ada yang terlewat. Untuk setiap fakta yang kamu temukan, susunlah dalam format bullet points untuk kemudahan pemahaman. Berikut detail kontennya: {content}

Catatan:
- Jika menemukan informasi yang ambigu atau memerlukan interpretasi, sertakan dengan catatan penjelasanmu.
- Usahakan untuk mempertahankan keakuratan dan kelengkapan informasi."""
    )

    outline_prompt = ChatPromptTemplate.from_template(
        """
Dengan menggunakan fakta-fakta yang telah diberikan: {facts}, klasifikasikan dan susunlah point-point penting dari konten dalam bahasa {language} menjadi sebuah outline terstruktur yang akan dijadikan panduan dalam menulis artikel. Ikuti langkah-langkah berikut untuk membuat outline yang efektif dan informatif:

1. **Tema dan Kategorisasi**: Identifikasi tema utama dalam konten berdasarkan fakta yang disediakan. Kategorikan fakta-fakta tersebut ke dalam tema-tema relevan yang akan menjadi bagian utama dari artikel.

2. **Alur Konten**: Tentukan urutan logis dari konten, dari pengenalan, pengembangan ide, hingga kesimpulan, berdasarkan tema-tema tersebut. Urutan ini harus memandu pembaca melalui artikel dengan alur yang mudah diikuti.

3. **Struktur Outline**: Buatlah outline yang mencakup semua tema utama dan subtema dengan fakta-fakta pendukung di setiap bagian. Untuk setiap tema dan subtema:
   - Sertakan judul bagian yang jelas dan deskriptif.
   - Tuliskan fakta-fakta kunci yang mendukung setiap tema/subtema.
   - Berikan penjelasan singkat bagaimana setiap fakta mendukung poin utama atau menyediakan konteks tambahan.

4. **Panduan Penulisan**: Pastikan bahwa setiap bagian outline disertai dengan instruksi atau saran tentang cara mengintegrasikan fakta-fakta tersebut ke dalam narasi artikel. Ini termasuk saran untuk transisi antar bagian, penggunaan data atau kutipan untuk memperkuat argumen, dan tips untuk menjaga keterlibatan pembaca.

Catatan Penting:
- Outline harus komprehensif namun ringkas, memberikan panduan yang jelas namun fleksibel untuk penulis.
- Jika menemukan fakta yang ambigu atau memiliki beberapa interpretasi, tentukan posisi terbaiknya dalam outline dan jelaskan mengapa ini relevan untuk bagian tersebut.
- Outline harus berfungsi sebagai kerangka kerja yang memudahkan penulis dalam mengembangkan setiap bagian artikel dengan fakta yang logis dan terstruktur.

Tujuan akhir dari outline ini adalah untuk memastikan bahwa penulis dapat menghasilkan artikel yang informatif, menarik, dan koheren, yang dengan jelas menyampaikan semua fakta penting kepada pembaca.
"""
    )

    # article_prompt = ChatPromptTemplate.from_template(
    #     """Buatkan saya artikel SEO friendly dari konten yang diberikan dalam bahasa {language}. Buatlah artikel yang menarik dan informatif. Berikan saya artikel yang memiliki panjang minimal 1000 kata. Buatlah berdasarkan alur dan outline berikut: {outline}

    #     Perhatikan ini, saya ingin kamu membuatnya dalam format markdown. Setiap bagian, harus memiliki minimal 2 paragraf. Jangan lupa untuk memasukkan fakta-fakta yang telah kamu buat sebelumnya dan susun menggunakan argumentasi yang logis. Berikut adalah informasi yang akan kamu gunakan: {facts}"""
    # )

    model_parser = llm | StrOutputParser()

    create_article = (
        {"content": RunnablePassthrough(), "language": RunnablePassthrough()}
        | facts_prompt
        | {"facts": model_parser, "language": RunnablePassthrough()}
        | outline_prompt
        | model_parser
    )

    result = create_article.invoke({"content": content, "language": "indonesia"})
    return {
        "result": result,
    }
