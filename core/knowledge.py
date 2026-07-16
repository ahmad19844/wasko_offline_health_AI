"""
core/knowledge.py

WASKO Health AI v3.0
Knowledge Base Engine

Responsibilities
----------------
✓ Load English markdown files
✓ Load Hausa markdown files
✓ Parse markdown sections
✓ Retrieve only requested section
✓ No random searching
"""

from pathlib import Path
import re

from config import KB_EN, KB_HA
from core.translator import translator


class KnowledgeBase:

    def __init__(self):

        # =====================================================
        # Knowledge Storage
        # =====================================================

        self.documents = {

            "English": {},

            "Hausa": {}

        }

        # =====================================================
        # Section Mapping
        # =====================================================

        self.section_map = {

            "English": {

                "overview": "Overview",
                "causes": "Causes",
                "symptoms": "Symptoms",
                "diagnosis": "Diagnosis",
                "treatment": "Treatment",
                "prevention": "Prevention",
                "complications": "Complications",
                "emergency": "Emergency"

            },

            "Hausa": {

                "overview": "Bayani",
                "causes": "Dalilai",
                "symptoms": "Alamomi",
                "diagnosis": "Gwaji",
                "treatment": "Magani",
                "prevention": "Rigakafi",
                "complications": "Matsaloli",
                "emergency": "Gaggawa"

            }

        }

        # =====================================================
        # Filename Mapping
        # =====================================================

        self.file_map = {

            "English": {

                "malaria": "malaria",
                "cholera": "cholera",
                "diabetes": "diabetes",
                "hypertension": "hypertension",
                "tuberculosis": "tuberculosis",
                "pneumonia": "pneumonia",
                "typhoid": "typhoid",
                "hiv": "hiv_aids",
                "nutrition": "nutrition",
                "pregnancy": "pregnancy",
                "maternal_health": "maternal_health",
                "child_health": "child_health",
                "first_aid": "first_aid",
                "emergency": "emergency"

            },

            "Hausa": {

                "malaria": "malariya",
                "cholera": None,
                "diabetes": "diabetis",
                "hypertension": None,
                "tuberculosis": "tuberculosis",
                "pneumonia": "pneumonia",
                "typhoid": "typhoid",
                "hiv": "hiv",
                "nutrition": None,
                "pregnancy": None,
                "maternal_health": None,
                "child_health": "child",
                "first_aid": "firstaid",
                "emergency": None

            }

        }

        self.load_documents()
    # =====================================================
    # Load All Documents
    # =====================================================

    def load_documents(self):
        """
        Load all markdown documents into memory.
        """

        self.documents = {
            "English": {},
            "Hausa": {}
        }

        self._load_language(
            language="English",
            folder=KB_EN
        )

        self._load_language(
            language="Hausa",
            folder=KB_HA
        )

        total = (
            len(self.documents["English"])
            +
            len(self.documents["Hausa"])
        )

        print(f"\nKnowledge Base Ready ({total} documents)")

    # =====================================================
    # Load One Language Folder
    # =====================================================

    def _load_language(
        self,
        language,
        folder
    ):
        """
        Load every markdown file in one language folder.
        """

        print(f"\nLoading {language} documents...")

        print(f"Folder: {folder}")

        if not folder.exists():

            print("Folder not found.")

            return

        count = 0

        reverse_map = {}

        for disease, filename in self.file_map[language].items():

            if filename:

                reverse_map[filename] = disease

        for file in sorted(folder.glob("*.md")):

            try:

                with open(

                    file,

                    "r",

                    encoding="utf-8"

                ) as f:

                    markdown = f.read()

                filename = file.stem.lower()

                disease = reverse_map.get(

                    filename,

                    filename

                )

                self.documents[language][disease] = (

                    self._parse_markdown(

                        markdown,

                        language

                    )

                )

                count += 1

                print(f"✓ {file.name}")

            except Exception as e:

                print(

                    f"✗ Failed to load {file.name}: {e}"

                )

        print(f"{language}: {count} documents loaded.")

    # =====================================================
    # Parse Markdown
    # =====================================================

    def _parse_markdown(
        self,
        markdown,
        language
    ):
        """
        Convert markdown into sections.

        Returns

        {
            overview: "...",
            causes: "...",
            symptoms: "...",
            ...
        }
        """

        sections = {}

        headings = self.section_map[language]

        for key, heading in headings.items():

            pattern = (

                rf"^##\s+{re.escape(heading)}\s*$"

            )

            match = re.search(

                pattern,

                markdown,

                flags=re.MULTILINE | re.IGNORECASE

            )

            if not match:

                continue

            start = match.end()

            next_heading = re.search(

                r"^##\s+",

                markdown[start:],

                flags=re.MULTILINE

            )

            if next_heading:

                end = start + next_heading.start()

            else:

                end = len(markdown)

            text = markdown[start:end].strip()

            sections[key] = text

        return sections
    #===================================================
    # update
    #===================================================

    def is_keyword_only(self, question):
        
        words = question.strip().split()

        return len(words) == 1


    # =====================================================
    # Retrieve Section
    # =====================================================

    def retrieve(
        self,
        question,
        selected_language="Auto"
    ):

        analysis = translator.analyze(
            question,
            selected_language
        )

        language = analysis["language"]
        disease = analysis["disease"]
        section = analysis["section"]

        document = self.get_document(
            disease,
            language
        )

        if not document:
            return ""

        if analysis.get("keyword_only", False):
            overview = document.get("overview", "")
            return "".join(overview.split("")[:6])

        return document.get(
            section,
            document.get("overview", "")
        )

    # =====================================================
    # Compatibility Wrapper
    # =====================================================

    def retrieve_context(
        self,
        query,
        language="Auto",
        top_k=3
    ):
        """
        Backwards-compatible wrapper.
        """

        return self.retrieve(
            question=query,
            selected_language=language
        )

    # =====================================================
    # Check Document Exists
    # =====================================================

    def has_document(
        self,
        disease,
        language="English"
    ):

        disease = translator.get_canonical_name(
            disease
        )

        return disease in self.documents.get(
            language,
            {}
        )

    # =====================================================
    # Get Document
    # =====================================================

    def get_document(
        self,
        disease,
        language
    ):

        docs = self.documents.get(language, {})

        if not disease:
            return None

        disease = disease.lower().strip()

        for name, content in docs.items():
            if name.lower() == disease:
                return content

        return None

    # =====================================================
    # List Document Names
    # =====================================================

    def document_names(
        self,
        language="English"
    ):

        return sorted(

            self.documents.get(
                language,
                {}
            ).keys()

        )

    # =====================================================
    # Statistics
    # =====================================================

    #def stats(self):

        #english = len(
         #   self.documents["English"]
        #)

        #hausa = len(
        #    self.documents["Hausa"]
       # )

       # return {

      #      "English": english,

     #       "Hausa": hausa,

    #        "Total": english + hausa

   # }
    
    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):
        """
        Return knowledge base statistics.
        """

        english = len(
            self.documents.get(
                "English",
                {}
            )
        )

        hausa = len(
            self.documents.get(
                "Hausa",
                {}
            )
        )

        return {
            "English": english,
            "Hausa": hausa,
            "Total": english + hausa
        }

    # =====================================================
    # Reload Knowledge Base
    # =====================================================

    def reload(self):

        self.load_documents()
# =====================================================
# Singleton Instance
# =====================================================

knowledge = KnowledgeBase()
