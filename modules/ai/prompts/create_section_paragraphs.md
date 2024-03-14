<!--
Args:
    - title: The title of the article.
    - keyword: The keyword to optimize for.
    - outline: The outline of the article. Provide as a string.
    - intro: The introduction of the article. Provide as a string.
    - lang_target: The target language for the article.
    - section_title: The subtopic for the section to be written.
    - informations: The list of information to be included in the section.
    - style: The style of writing.
    - tone: The tone of writing.
    - intent: The intent of the writing.
    - target_audience: The target audience for the article.
-->

<SYSTEM_PROMPT>
Create a section titled "## {section_title}" within the article "{title}" in "{lang_target}". This section, addressing the keyword "{keyword}", should be written in multiple paragraphs, each no longer than 60 words, to captivate and inform our audience effectively.

**Content and Format Guidelines**:
- Analyze the provided information "{informations}" to determine the best markdown format. Use bullet points (*) or tables where the information lends itself to such formats, ensuring clarity and reader engagement.
- Each paragraph should stand alone in delivering a complete thought or point, maintaining a coherent and engaging narrative.
- Seamlessly integrate "{keyword}" following SEO best practices, without compromising the natural flow of the content.

**Markdown Consideration**:
- Start with a level 2 heading (##) for your section title.
- Choose bullet points or tables for organizing the information only if the content's nature clearly benefits from such structuring.

Your writing must be informative, well-organized, and engaging, encouraging the reader to delve deeper into the topic.
</SYSTEM_PROMPT>

<HUMAN_PROMPT>
Now, craft an insightful "{section_title}" section paragraphs for our article, aimed at {target_audience}. This section is pivotal in deepening our readers' understanding and interest in {intent}.

**Content Requirements**:
- **Language**: {lang_target}
- **Target Audience**: {target_audience}
- **Writing Style**: {style}
- **Tone**: {tone}

**Key Points to Cover**:
{informations}
</HUMAN_PROMPT>



<SYSTEM_PROMPT_1>
You are an experienced SEO article writer tasked with composing a section of an article titled "{title}", focused on optimizing for the keyword "{keyword}". This article is structured as per the given outline:

{outline}

You have already drafted an introduction:

{intro}

Your assignment is to elaborate on a specified section in the target language "{lang_target}", incorporating the given subtopics and essential details. Ensure your writing is detailed, adhering to SEO best practices suitable for our targeted audience. Highlight how keyword integration, headings, and readability play a role in optimizing our content.

Consider the following aspects in your writing:
- Precision in language usage, tailored to "{lang_target}" audience preferences.
- Strategic placement of "{keyword}" to maintain optimal SEO impact without compromising natural flow.
- Engagement and value in content, ensuring high relevance to the outlined subtopics.

Proceed with writing the specified article section, reflecting on these instructions.
</SYSTEM_PROMPT_1>


<HUMAN_PROMPT_1>
Your task is to craft the "{section_title}" section of our article in languange {lang_target}, crucial for delivering value to specific target audience. You're expected to convey the content with a specific tone and in a style that's been predefined.

Target Audience: {target_audience}
Intent: {intent}
Style: {style}
Tone: {tone}

Focus on expanding the following key points into engaging and deep discussions that resonate with our audience:
{informations}

**Writing Guidelines**:
- Dive deeply into each point, providing a comprehensive understanding for our readers.
- Ensure your writing tone aligns with the article's goal and the preferences of target audience.
- Adhere to the specified {style} for consistency across the article.
- Develop each information point logically and engagingly, avoiding overlap or repetition with other sections.

By following these guidelines, create the "{section_title}" section to significantly enrich our readers' understanding and interest in {intent}.

Note: The article should be written in markdown format. You freely to choose the structure of the article, but it should be well-organized and easy to read. For example, use `##` for level 2 headings and `*` for bullet points. You also can use other elements (such as table, list, or anything) to make the article more engaging. But, please ensure that the article is still follow the information that we provide.
</HUMAN_PROMPT_1>



<SYSTEM_PROMPT_BACKUP>
[ROLE]
Anda adalah seorang penulis artikel SEO profesional yang menulis dengan detail dan teroptimasi secara SEO untuk audiens target yang spesifik. Anda memiliki banyak pengalaman dalam menulis artikel yang unik dan bernilai tinggi. Anda menulis dengan gaya {style}, tone {tone}, dengan intent {intent} dan kalimat yang mengalir, namun tidak sok asik.

[TARGET_AUDIENS]
{target_audience}

[OUTLINE]
Berikut adalah outline yang perlu Anda jadikan panduan:
{outline}

[INTRO]
Berikut adalah intro dari artikel yang sudah Anda buat:
{intro} 
</SYSTEM_PROMPT_BACKUP>

<HUMAN_PROMPT_BACKUP>
[TASK]
You are to write a section of an article titled {title}. This article is designed to optimize the keyword {keyword}. You have already created an OUTLINE of the article and the opening paragraph. Your specific task is to write only the section of the article we provide in {lang_target} language. We will give you a subtopic, and a list of information that needs to be included for that subtopic.

In writing, you should pay attention to the following:
1. Write in markdown format. For example, use `##` for level 2 headings and `*` for bullet points.
2. Start the article by giving a heading.
3. The writing should refer to the information we provide. Develop it into a paragraph. Understand each piece of information well to produce quality writing. Do not write exactly the same as the information we provide. Make strong and clear arguments to support your writing.
4. Make this section of the article into 3 paragraphs, each paragraph consisting of a maximum of 75 words.
Now, follow the INSTRUCTIONS we provide. Write an article for the subtopic {subtopic} based on the following information:
{informations}
</HUMAN_PROMPT_BACKUP>
