"""
retriever.py
"""

from core.knowledge import knowledge


class Retriever:

    def retrieve(

        self,

        query,

        language="English"

    ):

        return knowledge.retrieve_context(

            query,

            language

        )

    def search(

        self,

        query,

        language="English"

    ):

        return knowledge.search(

            query,

            language

        )


retriever = Retriever()
