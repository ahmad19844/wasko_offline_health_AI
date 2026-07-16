"""
core/prompt_builder.py

WASKO Health AI
TinyLlama Prompt Builder

Builds short prompts for TinyLlama.
"""

import re


class PromptBuilder:

    def __init__(self):

        self.max_context_chars = 1200
    # ==================================================
    # Clean Context
    # ==================================================

    def clean_context(
        self,
        context
    ):
        """
        Clean retrieved knowledge before
        sending it to TinyLlama.
        """

        if not context:

            return ""

        # Remove markdown headings

        context = re.sub(

            r"^#+.*$",

            "",

            context,

            flags=re.MULTILINE

        )

        # Remove multiple blank lines

        context = re.sub(

            r"\n{3,}",

            "\n\n",

            context

        )

        context = context.strip()

        return context[:self.max_context_chars]
    # ==================================================
    # System Prompt
    # ==================================================

    def system_prompt(
        self,
        language="English"
):
        if language == "Hausa":

            return (

                    "Kai WASKO Health AI ne, mataimakin lafiya mara amfani da intanet."
                    "Ka amsa tambayar mai amfani kawai. "
                    "Idan mai tambaya ya rubuta sunan cuta ko kalma daya kawai,"
                    "ka bada bayani na farko (overview) kawai cikin layi shida ko kasa. "
                    "Kada ka rubuta dukkan bayanin kundin lafiya. "
                    "Yi amfani da bayanin da aka bayar kawai. "
                    "Kada ka kirkiri bayanai. "
                    "Kada ka kara bayanin da ba a tambaya ba. "
                    "Kada ka yi amfani da Markdown, alamu, ko taken rubutu. "
                    "Yi amfani da Hausa mai sauki."
              ) 

            return (

                    "You are WASKO Health AI, an offline medical assistant. "
                    "Answer ONLY the user's question. "
                    "Use ONLY the provided medical context by the user. "
                    "Do NOT use Markdown formatting or add any content that you are not ask. "
                    "Do NOT use bold (**), italics (*), headings (#), bullet points (-, *, •), or numbered lists. "
                    "Return plain text only. "
                    "If the user asks about causes, answer only the causes. "
                    "If the user enters only a disease name, return only a short overview in no more than six lines. "
                    "Do not add introductions, conclusions, sources, copyright, or application information."

          )
    # ==================================================
    # Build Prompt
    # ==================================================

    def build_prompt(
        self,
        question,
        context,
        language="English"
    ):

        context = self.clean_context(
            context
        )

        if language == "Hausa":

            return f"""
Bayanin lafiya:

{context}

Tambaya:

{question}

Umarni:

Amsa tambayar kawai.

Kada ka maimaita bayanin.

Yi amfani da Hausa mai sauki.

Amsa cikin kalmomi 120 kacal.
"""

        return f"""
Medical Context:

{context}

Question:

{question}

Instructions:

Answer only the user's question.

Use only the medical context.

Do not repeat the context.

Do not use markdown headings.

Maximum 120 words.
"""
    # ==================================================
    # Compatibility Wrapper
    # ==================================================

    def build_user_prompt(
        self,
        question,
        context,
        language="English"
    ):

        return self.build_prompt(
            question=question,
            context=context,
            language=language
        )
# ==================================================
# Singleton
# ==================================================

prompt_builder = PromptBuilder()
