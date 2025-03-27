from ast import pattern
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern
import re


def find_matches(patterns, text, supported_entity):

    matches = []
    for pat in patterns:
        for match in re.finditer(pat.pattern, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": supported_entity,
                "score": pat.score,
            })
    return matches


class AddressRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("ADDRESS", r"\d{1,5}\s([A-Za-z0-9#,.&'-]+\s)+(?:\s(?:Apt|Suite|Unit|#)\s?\d+[a-zA-Z]?,?)?"
                            + r"\s?[a-zA-Z]?,?\s?[a-zA-Z]{2}\s\d{5}", score=1.0)]

        super().__init__(supported_entity="ADDRESS", patterns=patterns)

    def find(self, text, entities=None):
        return find_matches(self.patterns, text, self.supported_entity)
    
class DOBRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern(
            "DOB",
            r"(?i)"
            + r"(date of birth|dob|birth date|birth)"
            + r"\s?:?\s?"
            + r"("
                + r"\d{1,2}/\d{1,2}/\d{4}|"
                + r"\d{4}/\d{1,2}/\d{1,2}|"
                + r"\d{1,2}-\d{1,2}-\d{4}|"
                + r"\d{1,2}\.\d{1,2}\.\d{4}|"
                + r"\d{4}\.\d{1,2}\.\d{1,2}|"
                + r"\d{4}-\d{1,2}-\d{1,2}|"
                + r"\d{8}|"
                + r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|"
                + r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}|"
                + r"\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}|"
                + r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}"
            + r")",
            score=1.0,
        )]

        super().__init__(supported_entity="DOB", patterns=patterns)

    def find(self, text, entities=None):
        return find_matches(self.patterns, text, self.supported_entity)

        

class TitleRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("TITLE", r"\b(Mr|Mrs|Ms|Mx|Dr|Prof)\.?\b", score=1.0)]

        super().__init__(supported_entity="TITLE", patterns=patterns)
    
    def find(self, text, entities=None):
        return find_matches(self.patterns, text, self.supported_entity)

class PostNominalRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("POSTNOMINAL", r"\b(PhD|MD|JD|DVM|DDS|CPA|RN|DO|MBBS|BSN|MSN|DNP|NP|CRNA|PA-C|PT|OT|SLP|FACP|FAAFP|FACS|FAAN|DMD|BDS|MS|FAGD|MAGD|ABGD|ABPD|ABOP|ABOMS|ABP|ABO|RDH|EFDA)\b", score=1.0)]

        super().__init__(supported_entity="POSTNOMINAL", patterns=patterns)

    def find(self, text, entities=None):
            return find_matches(self.patterns, text, self.supported_entity)
        
class SSNRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern("SSN",r"((\*\*\*\-\*\d\-\d{4})|(\d{3}\-\d{2}\-\d{4}))\b",score=1.0)
        ]
        super().__init__(supported_entity="SSN", patterns=patterns)

    def find(self, text, entities=None):
        return find_matches(self.patterns, text, self.supported_entity)
    
class MedicaidAccountRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern("MEDICAID_ACCOUNT", r"\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b", score=1.0)
        ]
        super().__init__(supported_entity="MEDICAID_ACCOUNT", patterns=patterns)

    def find(self, text, entities=None):
        return find_matches(self.patterns, text, self.supported_entity)
