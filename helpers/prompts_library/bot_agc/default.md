# [STEP 1] - Article to Information List
Extract the main points from the source article.
**Input:**
- `original_article`: The source article that will be used to generate the new article.

**Output:**
- `informations`: The main points that have been extracted from the source article.

### **PROMPTS**:
```markdown
I need your assistance to deeply analyze the following text. Please identify and summarize every key point in great detail, including any minor or seemingly trivial information. Your goal is to overlook no detail, presenting the information completely in a bullet-point format:

- Complete and detailed information for point 1
- Complete and detailed information for point 2
- Complete and detailed information for point 3
...
- Complete and detailed information for point n

Ensure to consider every aspect of the text as you compile this list of key points:
`{original_article}`
```


# [STEP 2] - Information to Outline
Generate an outline based on the created main points.
**Input:**
- `lang_source`: The language code of the source article
- `lang_target`: The language code of the target article. 
- `informations`: List of informations that have been extracted from the source article.

**Output:**
- An outline with the json format which contains the following structure:
    - `intro`: The introduction explanation of the article.
    - `sections`: The list of sections in to be written in the article. Each section contains:
        - `subheading`: The subheading of the section.
        - `information`: The list of relevant information of the section from the `informations` input.


### **SYSTEM_PROMPTS**:
```markdown
As an SEO article outline specialist, transform the information from `{lang_source}` into an organized outline for an article in `{lang_target}`. Follow these steps:

1. **Theme Identification**: Pinpoint major themes within the information.
2. **Information Grouping**: Sort the details under each theme, focusing on key points.
3. **Outline Structuring**: Rearrange themes for a logical flow, independent of the original text structure. Ensure all vital information is included.
4. **Finalizing Outline**: Confirm the outline is comprehensive and logically structured, ready for SEO article writing in `{lang_target}`.

Emphasize creating a content-rich and logically sequenced article outline, transitioning insights from `{lang_source}` to `{lang_target}` effectively.
```

### **HUMAN_PROMPTS**:
```markdown
This is the facts and information you need to create an outline:
`{informations}`
```

# [STEP 3] - Outline to SEO Data and Writing Guidelines
Generate the SEO data and writing guidelines using the created outline.
**Input:**
- `outline`: The outline that has been created in the previous step. Must be in string format.
- `lang_target`: The target language for the output.

**Output:**
- `keyword`: Main keyword for the article.
- `seo_title`: The SEO title for the article.
- `meta_description`: The meta description for the article.
- `target_audience`: The target audience for the article.
- `intent`: The intent of the article.
- `style`: The writing style for the article.
- `tone`: The tone of the article.

### **SYSTEM_PROMPTS**:
```markdown
[INSTRUCTIONS]
You are an experienced SEO specialist. Your task is to analyze an article outline and provide a guide for writing the article.  You need to determine the following:
1. The primary keyword.
2. SEO-friendly title.
3. SEO-friendly meta description.
4. Writing guidelines, including intent, style and tone.
```

### **HUMAN_PROMPTS**:
```markdown
[OUTPUT]
FORMAT: JSON format as per the predetermined structure.
LANGUAGE: All data outputs should be in `{lang_target}`.

[OUTLINE]
`{outline}`
```
"keyword": args.keyword,
"title": args.title,
"description": args.description,
"lang_target": args.lang_target,
"intro_guideline": args.intro_guideline,
"intent": args.intent,
"style": args.style,
"tone": args.tone,

# [STEP 4] - Create an Introduction
Create an introduction based on the outline, SEO data, and writing guidelines.
**Input:**
- `keyword`: Main keyword for the article generated in STEP 3.
- `title`: The `seo_title` for the article generated in STEP 3
- `description`: The `meta_description` for the article generated in STEP 3
- `lang_target`: The target language for the output.
- `intro_guideline`: The `intro` guideline from the outline generated in STEP 2.
- `intent`: The `intent` for the article generated in STEP 3.
- `style`: The `style` for the article generated in STEP 3.
- `tone`: The `tone` for the article generated in STEP 3.

**Output:**
- `introduction`: The introduction of the article.

### **SYSTEM_PROMPTS**:
```markdown
[INSTRUCTIONS]
Sebagai penulis SEO berpengalaman, tugas kamu adalah menulis dua paragraf pembuka dalam bahasa `{lang_target}` untuk artikel dengan judul `{title}`. Artikel ini ditujukan untuk menarget kata kunci `{keyword}`. Meta deskripsi untuk artikel ini adalah:

`{description}`

Paragraf pembuka harus dirancang untuk menarik perhatian pembaca dan mendorong mereka untuk melanjutkan membaca artikel. Gunakan meta deskripsi sebagai panduan untuk menentukan informasi apa yang harus disertakan dalam paragraf pembuka. Setiap paragraf tidak boleh lebih dari 200 karakter.

Dalam menulis paragraf pembuka, pastikan untuk mematuhi panduan penulisan berikut:
- Intensi: `{intent}`
- Gaya: `{style}`
- Tone: `{tone}`

Pastikan juga untuk menyertakan kata kunci `{keyword}` dalam salah satu paragraf. Selain itu, berikan sedikit latar belakang atau konteks tentang topik artikel untuk membantu pembaca memahami apa yang akan mereka baca.
```

### **HUMAN_PROMPTS**:
```markdown
[INTRO GUIDELINES]
Berikut adalah gambaran umum dari intro yang perlu kamu buat:
`{intro_guideline}`
```

# [STEP 5] - Write the section body (Loop through the outline)
Loop through the outline and generate the content for each point. This process use the outline to inform the bot about the whole article structure, so the bot can generate the content for each point based on the writing guidelines, eventhough the bot only have the main points of the current section.
**Input:**
- `outline`: The outline that has been created in the previous STEP 2. Must be in string format.
- `intro`: The introduction that has been created in the previous STEP 4. Must be in string format.
- `lang_target`: The target language for the output.
- `keyword`: Main keyword for the article generated in STEP 3.
- `title`: The `seo_title` for the article generated in STEP 3
- `target_audience`: The target audience for the article generated in STEP 3.
- `intent`: The `intent` for the article generated in STEP 3.
- `style`: The `style` for the article generated in STEP 3.
- `tone`: The `tone` for the article generated in STEP 3.
- `section_title`: The title of the section that will be written. Get from the outline.
- `informations`: The list of relevant information of the section from the `informations` input. Get from the outline.

**Output:**
- `section_content`: The content of the section.

### **SYSTEM_PROMPTS**:
```markdown
Create a section titled "## `{section_title}`" within the article "`{title}`" in "`{lang_target}`". This section, addressing the keyword "`{keyword}`", should be written in multiple paragraphs, each no longer than 60 words, to captivate and inform our audience effectively.

**Content and Format Guidelines**:
- Analyze the provided information "`{informations}`" to determine the best markdown format. Use bullet points (*) or tables where the information lends itself to such formats, ensuring clarity and reader engagement.
- Each paragraph should stand alone in delivering a complete thought or point, maintaining a coherent and engaging narrative.
- Seamlessly integrate "`{keyword}`" following SEO best practices, without compromising the natural flow of the content.

**Markdown Consideration**:
- Start with a level 2 heading (##) for your section title.
- Choose bullet points or tables for organizing the information only if the content's nature clearly benefits from such structuring.

Your writing must be informative, well-organized, and engaging, encouraging the reader to delve deeper into the topic.
```

### **HUMAN_PROMPTS**:
```markdown
Now, craft an insightful "`{section_title}`" section paragraphs for our article, aimed at `{target_audience}`. This section is pivotal in deepening our readers' understanding and interest in `{intent}`.

**Content Requirements**:
- **Language**: `{lang_target}`
- **Target Audience**: `{target_audience}`
- **Writing Style**: `{style}`
- **Tone**: `{tone}`

**Key Points to Cover**:
`{informations}`
```

### [ADDITONAL NOTES]
For every loop in STEP_5, the script also contains the instructions to generate the search image query to be used as the keyword for the image search. The search image query will be generated based on the content of the section that has been generated in STEP_5. 
**Input**:
- `text`: The content of the section that has been generated in STEP_5.

**Output**:
- `query`: The search image query that represents the content of the section with the format [IMAGE QUERY]<query>[/IMAGE QUERY].

### **PROMPTS**:
```markdown
Generate ONLY ONE concise, detailed ENGLISH search queries for the provided text. Ensure queries are straightforward for use in common image search engines, reflecting the given text or article. Focus on relevance and specificity without additional explanations.

Here is the summary:
{text}

Ensure the output wraps with [IMAGE QUERY]<query>[/IMAGE QUERY]

Example Output 1:
[IMAGE QUERY]A group of people playing soccer in a stadium[/IMAGE QUERY]

Example Output 2:
[IMAGE QUERY]A close-up of a cat with green eyes[/IMAGE QUERY]

Example Output 3:
[IMAGE QUERY]The Eiffel Tower at night[/IMAGE QUERY]
```
