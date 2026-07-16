"""
core/translator.py

WASKO Health AI v3.0
Query Analyzer

Responsibilities
----------------
✓ Detect language
✓ Normalize user queries
✓ Detect disease/topic
✓ Detect requested section
✓ Extract keywords
✓ Prepare structured query analysis
"""

import re


class Translator:

    def __init__(self):

        # ==========================================================
        # Supported Languages
        # ==========================================================

        self.languages = [
            "English",
            "Hausa"
        ]

        # ==========================================================
        # Disease Aliases
        #
        # Every possible spelling maps to ONE canonical name.
        # ==========================================================

        self.disease_aliases = {

            # ---------- English ----------

            "malaria": "malaria",

            "typhoid": "typhoid",

            "cholera": "cholera",

            "diabetes": "diabetes",

            "hypertension": "hypertension",

            "high blood pressure": "hypertension",

            "blood pressure": "hypertension",

            "bp": "hypertension",

            "hbp": "hypertension",

            "tuberculosis": "tuberculosis",

            "tb": "tuberculosis",

            "pneumonia": "pneumonia",

            "pregnancy": "pregnancy",

            "maternal health": "maternal_health",

            "nutrition": "nutrition",

            "child health": "child_health",

            "first aid": "first_aid",

            "emergency": "emergency",

            "hiv": "hiv",

            "aids": "hiv",

            "hiv aids": "hiv",


            # ---------- Hausa ----------

            "malariya": "malaria",

            "zazzabin cizon sauro": "malaria",

            "zazzabin sauro": "malaria",

            "ciwon sukari": "diabetes",

            "suga": "diabetes",

            "hawan jini": "hypertension",

            "tarin fuka": "tuberculosis",

            "cutar tarin fuka": "tuberculosis",

            "zazzabin taifod": "typhoid",

            "taifod": "typhoid",

            "kwalara": "cholera",

            "cutar kanjamau": "hiv",

            "kanjamau": "hiv",

            "cutar huhu": "pneumonia",

            "ciki": "pregnancy",

            "lafiyar uwa": "maternal_health",

            "abinci mai gina jiki": "nutrition",

            "lafiyar yara": "child_health",

            "agajin farko": "first_aid",

            "gaggawa": "emergency"

        }

        # ==========================================================
        # Section Aliases
        #
        # Used to locate the correct section inside markdown.
        # ==========================================================

        self.section_aliases = {

            "overview": [

                "what is",
                "what's",
                "define",
                "definition",
                "meaning",
                "overview",
                "about",
                "tell me about",
                "explain",
                "introduction",


                "menene",
                "mene ne",
                "ma'ana",
                "bayani",
                "wani bayani"

            ],

            "causes": [
                "cause",
                "causes",
                "why",
                "reason",
                "origin",
                "how do you get",
                "how do people get",
                "spread",
                "transmission",
                "me yake jawo",
                "me ke haifar",
                "dalili",
                "dalilai",
                "haddasa"

 ],

            "symptoms": [

                "symptom",
                "symptoms",
                "sign",
                "signs",

                "alama",
                "alamomi"

            ],

            "diagnosis": [

                "diagnosis",
                "diagnose",

                "gwaji",
                "bincike"

            ],

            "treatment": [

                "treat",
                "treatment",
                "medicine",
                "medication",
                "drug",
                "cure",
                "manage",

                "magani",
                "yaya ake magani",
                "yadda ake magani"

            ],

            "prevention": [

                "prevent",
                "prevention",

                "rigakafi",
                "kaucewa"

            ],

            "complications": [

                "complication",
                "complications",
                "effects",

                "matsala",
                "matsaloli"

            ],

            "emergency": [

                "emergency",
                "urgent",

                "gaggawa"

            ]

        }
    # ==========================================================
    # Detect Language
    # ==========================================================

    def detect_language(
        self,
        question,
        selected_language="Auto"
    ):
        """
        Detect which language should be used.

        Priority:
        1. User selected English/Hausa
        2. Auto detect from question
        """

        if selected_language in ("English", "Hausa"):
            return selected_language

        question = question.lower()

        hausa_words = [

            "menene",
            "mene",
            "malariya",
            "alamomi",
            "dalili",
            "dalilai",
            "magani",
            "rigakafi",
            "gwaji",
            "hawan",
            "jini",
            "ciwon",
            "tarin",
            "fuka",
            "kanjamau",
            "kwalara",
            "gaggawa",
            "yaya",
            "wani",
            "wace",
            "ina",
            "yaushe",
            "ta yaya"

        ]

        for word in hausa_words:

            if word in question:

                return "Hausa"

        return "English"

    # ==========================================================
    # Normalize Query
    # ==========================================================

    def normalize_query(
        self,
        question
    ):
        """
        Convert different spellings into a
        standard internal representation.
        """

        question = question.lower().strip()

        question = re.sub(
            r"\s+",
            " ",
            question
        )

        for alias, canonical in self.disease_aliases.items():
            question = question.replace(
                    alias,
                    canonical
            )

        return question

    # ==========================================================
    # Detect Disease
    # ==========================================================

    def detect_disease(
        self,
        question
    ):
        """
        Return the canonical disease name.
        """

        question = self.normalize_query(question)

        for disease in sorted(

            set(self.disease_aliases.values()),

            key=len,

            reverse=True

        ):

            if disease in question:

                return disease

        return None

    # ==========================================================
    # Extract Keywords
    # ==========================================================

    def extract_keywords(
        self,
        question
    ):
        """
        Return only meaningful keywords.
        """

        question = self.normalize_query(question)

        words = re.findall(

            r"[a-zA-ZÀ-ÿ]+",

            question

        )

        stop_words = {

            # English

            "what",
            "is",
            "are",
            "the",
            "of",
            "for",
            "to",
            "and",
            "or",
            "about",
            "tell",
            "me",
            "can",
            "you",
            "how",
            "why",
            "does",
            "do",

            # Hausa

            "menene",
            "mene",
            "na",
            "da",
            "ta",
            "ne",
            "ce",
            "ake",
            "ina",
            "shi",
            "ita",
            "su",
            "ko"

        }

        keywords = []

        disease = self.detect_disease(question)

        if disease:

            keywords.append(disease)

        for word in words:

            if len(word) < 3:
                continue

            if word in stop_words:
                continue

            if word not in keywords:

                keywords.append(word)

        return keywords
  #================================================
  # keyord
  #==================================================

    def is_keyword_only(self, question):
        """
        Returns True if the user entered only
        one medical keyword.
        """
        normalized = self.normalize_query(question)
        words = normalized.split()
        return len(words) == 1


    # ==========================================================
    # Detect Requested Section
    # ==========================================================

    def detect_section(
        self,
        question
    ):
        """
        Determine which section of the medical
        document the user is asking for.

        Default:
            overview
        """

        question = self.normalize_query(question)

        for section, aliases in self.section_aliases.items():

            for alias in aliases:

                if alias in question:

                    return section

        return "overview"

    # ==========================================================
    # Analyze User Question
    # ==========================================================

    def analyze(
        self,
        question,
        selected_language="Auto"
    ):
        """
        Analyze a user question and return a
        structured dictionary for retrieval.
        """

        language = self.detect_language(
            question,
            selected_language
        )

        normalized = self.normalize_query(question)

        disease = self.detect_disease(normalized)

        section = self.detect_section(normalized)

        keywords = self.extract_keywords(normalized)

        return {
                "language": language,
                "question": question,
                "normalized": normalized,
                "disease": disease,
                "section": section,
                "keywords": keywords,
                "keyword_only": self.is_keyword_only(question)

        }

    # ==========================================================
    # Check if Emergency Question
    # ==========================================================

    def is_emergency(
        self,
        question
    ):
        """
        Detect emergency situations.
        """

        question = question.lower()

        emergency_words = [

            "cannot breathe",
            "difficulty breathing",
            "heart attack",
            "stroke",
            "seizure",
            "unconscious",
            "severe bleeding",

            "ba ya numfashi",
            "wahalar numfashi",
            "bugun zuciya",
            "ya suma",
            "farfadiya",
            "jini mai yawa"

        ]

        return any(
            word in question
            for word in emergency_words
        )

    # ==========================================================
    # Get Canonical Disease Name
    # ==========================================================

    def get_canonical_name(
        self,
        name
    ):
        """
        Convert any alias into the
        canonical disease name.
        """

        if not name:
            return None

        name = name.lower().strip()

        return self.disease_aliases.get(
            name,
            name
        )
# ==========================================================
# Singleton Instance
# ==========================================================

translator = Translator()
