"""
core/llm.py

WASKO Health AI
TinyLlama GGUF Interface
"""

from pathlib import Path

from llama_cpp import Llama

from config import (
    MODEL_PATH,
    MAX_NEW_TOKENS,
    MAX_CONTEXT_CHARS,
    TEMPERATURE,
    TOP_P,
    REPEAT_PENALTY,
)
class LocalLLM:

    def __init__(self):

        print("\nLoading TinyLlama...")

        self.max_context_chars = 1200

        self.max_new_tokens = MAX_NEW_TOKENS

        self.model = Llama(

            model_path=str(Path(MODEL_PATH)),

            n_ctx=1024,

            n_threads=4,

            n_batch=256,

            verbose=False

        )

        print("✓ TinyLlama Loaded")
    # ==================================================
    # Prevent Context Overflow
    # ==================================================

    def truncate_prompt(
        self,
        prompt
    ):

        if len(prompt) <= self.max_context_chars:

            return prompt

        return prompt[:self.max_context_chars]
    # ==================================================
    # Chat
    # ==================================================

    def chat(
        self,
        system_prompt,
        user_prompt
    ):

        prompt = f"""
{system_prompt}

{user_prompt}
"""

        prompt = self.truncate_prompt(
            prompt
        )

        output = self.model(

            prompt,

            max_tokens=self.max_new_tokens,

            temperature=0.3,

            top_p=0.9,

            repeat_penalty=1.15,

            stop=[

                "User:",

                "Question:",

                "Medical Context:"

            ]

        )

        return output["choices"][0]["text"].strip()
    def chat(
        self,
        system_prompt,
        user_prompt
    ):

        try:

            prompt = f"""
{system_prompt}

{user_prompt}
"""

            prompt = self.truncate_prompt(
                prompt
            )

            output = self.model(

                prompt,

                max_tokens=self.max_new_tokens,

                temperature=0.3,

                top_p=0.9,

                repeat_penalty=1.15,

                stop=[
                    "Question:",
                    "User:",
                    "Medical Context:"
                ]

            )

            return output["choices"][0]["text"].strip()

        except Exception as e:

            return f"Generation Error\n\n{e}"
llm = LocalLLM()
