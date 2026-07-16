"""
core/conversation.py

WASKO HEALTH AI
Conversation Controller
"""

import time
import traceback

import streamlit as st

from config import *
from core.translator import translator
from core.knowledge import knowledge
from core.prompt_builder import prompt_builder
from core.llm import llm
from PIL import Image


class Conversation:
    """
    Main controller for WASKO Health AI.
    Handles UI, session state and conversation flow.
    """

    def __init__(self):
        self.initialize_session()

    # ==================================================
    # Session State
    # ==================================================

    def initialize_session(self):
        """Initialize Streamlit session variables."""

        defaults = {
            "messages": [],
            "response_time": 0.0,
            "last_context": "",
            "last_analysis": None,
            "language": "Auto",
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    # ==================================================
    # Selected Language
    # ==================================================

    def selected_language(self):
        """Return selected language."""

        return st.session_state.get(
            "language",
            "Auto"
        )

    # ==================================================
    # Reset Chat
    # ==================================================

    def clear_chat(self):
        """Clear conversation history."""

        st.session_state.messages = []
        st.session_state.response_time = 0.0
        st.session_state.last_context = ""
        st.session_state.last_analysis = None

    # ==================================================
    # Add Message
    # ==================================================

    def add_message(
        self,
        role,
        content
    ):
        """Add a message to chat history."""

        st.session_state.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    # ==================================================
    # Save Retrieved Context
    # ==================================================

    def save_context(
        self,
        context,
        analysis=None
    ):
        """Save retrieved context."""

        st.session_state.last_context = context
        st.session_state.last_analysis = analysis

    # ==================================================
    # Sidebar
    # ==================================================

    def sidebar(self):

        with st.sidebar:

            st.title("🩺 WASKO AI Medical Assistant")

            st.divider()

            language = st.selectbox(
                "Language",
                [
                    "Auto",
                    "English",
                    "Hausa"
                ],
                index=[
                    "Auto",
                    "English",
                    "Hausa"
                ].index(
                    st.session_state.language
                )
            )

            st.session_state.language = language

            st.divider()

            stats = knowledge.stats()

            st.subheader("Knowledge Base")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "English",
                    stats.get("English", 0)
                )

            with col2:
                st.metric(
                    "Hausa",
                    stats.get("Hausa", 0)
                )

            st.metric(
                "Total",
                stats.get("Total", 0)
            )

            st.divider()

            st.subheader("System")

            st.write("Offline AI Medical Assistant")
            st.write("🔒 Runs completely offline")

            st.divider()

            st.subheader("Last Response")

            st.write(
                f"{st.session_state.response_time:.2f} sec"
            )

            st.divider()

            if st.button(
                "🗑 Clear Chat",
                use_container_width=True
            ):
                self.clear_chat()
                st.rerun()

            st.divider()

            st.caption(
                "Offline bilingual medical assistant powered by TinyLlama + RAG"
            )

    # ==================================================
    # Header
    # ==================================================

    def header(self):

        col1, col2 = st.columns([3, 1])
        
        with col1:

            st.title("🩺 WASKO Offline AI Medical Assistant")

        with col2:

            logo = Image.open("assets/hosp.png")
            st.image("assets/log.png", width=200)

    st.divider()

    # ==================================================
    # Display Messages
    # ==================================================

    def show_messages(self):
        """Display chat history."""

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

    # ==================================================
    # Chat Input
    # ==================================================

    def get_question(self):
        """Get user input."""

        return st.chat_input(
            "Ask a medical question..."
        )
    # ==================================================
    # Retrieve Knowledge
    # ==================================================

    def retrieve_knowledge(
        self,
        question,
        language
    ):
        """
        Retrieve relevant information from the offline
        knowledge base.
        """

        try:

            context = knowledge.retrieve(
                question=question,
                selected_language=language
            )

            if context:
                return context.strip()

            return ""

        except Exception:

            traceback.print_exc()

            return ""

    # ==================================================
    # Determine Whether LLM Is Needed
    # ==================================================

    def needs_llm(
        self,
        question
    ):
        """
        Determine whether the user is asking a question
        that requires reasoning rather than simple retrieval.
        """

        q = question.lower()

        keywords = [

            "compare",
            "difference",
            "summarize",
            "summary",
            "analyze",
            "analysis",
            "why",
            "how",

            "kwatanta",
            "bambanci",
            "takaita",
            "me yasa",
            "ta yaya"

        ]

        return any(word in q for word in keywords)

        """
        Determine whether the user is asking a question
        that requires reasoning rather than simple retrieval.
        """

        q = question.lower()

        keywords = [

            "compare",
            "difference",
            "summarize",
            "summary",
            "analyze",
            "analysis",
            "why",
            "how",

            "kwatanta",
            "bambanci",
            "takaita",
            "me yasa",
            "ta yaya"

        ]

        return any(word in q for word in keywords)

    # ==================================================
    # Generate Answer
    # ==================================================

    def generate_answer(
        self,
        question,
        language
    ):
        """
        Generate answer using the offline knowledge base.
        """

        start_time = time.time()

        try:

            context = self.retrieve_knowledge(
                question,
                language
            )

            self.save_context(
                context=context,
                analysis=None
            )

            if context:

                answer = self.clean_answer(context)

            else:

                if language == "Hausa":

                    answer = (
                        "Yi haƙuri. Ban sami bayanin wannan tambayar "
                        "a cikin kundin bayanan lafiyar WASKO ba."
                    )

                else:

                    answer = (
                        "Sorry, I couldn't find information "
                        "about that topic in the offline "
                        "medical knowledge base."
                    )

            st.session_state.response_time = (
                time.time() - start_time
            )

            return answer

        except Exception:

            st.session_state.response_time = (
                time.time() - start_time
            )

            traceback.print_exc()

            return (
                "An unexpected error occurred.\n\n"
                + traceback.format_exc()
            )

    # ==================================================
    # Assistant Response
    # ==================================================

    def assistant_response(
        self,
        question
    ):
        """
        Generate and display assistant response.
        """

        language = self.selected_language()

        answer = self.generate_answer(
            question,
            language
        )

        self.add_message(
            "assistant",
            answer
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

    # ==================================================
    # User Message
    # ==================================================

    def add_user_message(
        self,
        question
    ):
        """
        Display and save user message.
        """

        self.add_message(
            "user",
            question
        )

        with st.chat_message("user"):

            st.markdown(question)
    # ==================================================
    # Clean AI Answer
    # ==================================================

    def clean_answer(
        self,
        answer
    ):
        """
        Clean retrieved text before displaying it.
        """

        import re


        paragraphs = []

        for p in answer.split("\n\n"):

            p = p.strip()

            if p and p not in paragraphs:
                paragraphs.append(p)

        answer = "\n\n".join(paragraphs)

        return answer.strip()

    # ==================================================
    # Emergency Detection
    # ==================================================

    def emergency_response(
        self,
        question,
        language
    ):
        """
        Detect emergency medical situations.
        """

        try:

            if not translator.is_emergency(question):
                return None

        except Exception:
            return None

        if language == "Hausa":

            return (
                "⚠️ **GAGGAWAR LAFIYA**\n\n"
                "Alamomin da aka bayyana na iya nuna "
                "gaggawar matsalar lafiya.\n\n"
                "A garzaya da mara lafiya zuwa "
                "asibiti mafi kusa ko kuma a kira "
                "ma'aikatan lafiya nan da nan.\n\n"
                "**WASKO Health AI ba ya maye gurbin likita "
                "ko sabis na gaggawa.**"
            )

        return (
            "⚠️ **MEDICAL EMERGENCY**\n\n"
            "The symptoms described may indicate "
            "a medical emergency.\n\n"
            "Please go to the nearest hospital "
            "or contact emergency medical services "
            "immediately.\n\n"
            "**WASKO Health AI is not a substitute "
            "for emergency medical care.**"
        )

    # ==================================================
    # Process Question
    # ==================================================

    def process_question(
        self,
        question
    ):
        """
        Process a user's question and display the answer.
        """

        language = self.selected_language()

        # Check emergency first
        emergency = self.emergency_response(
            question,
            language
        )

        if emergency:

            answer = emergency

        else:

            answer = self.generate_answer(
                question,
                language
            )

            answer = self.clean_answer(answer)

            # Add source only if information was found
            if (
                "couldn't find" not in answer.lower()
                and
                "ban sami" not in answer.lower()
            ):

                answer += (
                    "\n\n---"
                    "\n📚 **Source:** Offline Knowledge Base"
                )

        self.add_message(
            "assistant",
            answer
        )

        with st.chat_message("assistant"):

            st.markdown(answer)
    # ==================================================
    # Main Application
    # ==================================================

    def run(self):
        """
        Main entry point for WASKO Health AI.
        """

        logo = Image.open("assets/hosp.png")
        st.set_page_config(
                page_title="WASKO OFFLINE AI MEDICAL ASSISTANT",
                page_icon=logo,
                layout="wide"
        )

        # Sidebar
        self.sidebar()

        # Header
        self.header()

        # Display previous messages
        self.show_messages()

        # Get user input
        question = self.get_question()

        if question:

            # Display user message
            self.add_user_message(question)

            # Generate assistant response
            self.process_question(question)

        st.divider()

        col1, col2 = st.columns([3, 1])

        with col1:

            st.caption(
                "© 2026 WASKO Health AI"
            )

            st.caption(
                "Offline English & Hausa Medical Assistant"
            )

        with col2:

            st.success("🟢 Offline")

        st.caption(
            f"⚡ Response Time: "
            f"{st.session_state.response_time:.2f} sec"
        )
