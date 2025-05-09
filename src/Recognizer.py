from ast import pattern
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern
import re


class BaseRegexRecognizer(PatternRecognizer):
    def find(self, text, entities=None):
        matches = []
        for pat in self.patterns:
            for match in re.finditer(pat.pattern, text):
                matches.append({
                    "start": match.start(),
                    "end": match.end(),
                    "entity_type": self.supported_entity,
                    "score": pat.score,
                })
        return matches


class AddressRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [Pattern("ADDRESS", r"\d{1,5}\s([A-Za-z0-9#,.&'-]+\s)+(?:\s(?:Apt|Suite|Unit|#)\s?\d+[a-zA-Z]?,?)?"
                            + r"\s?[a-zA-Z]?,?\s?[a-zA-Z]{2}\s\d{5}", score=1.0)]

        super().__init__(supported_entity="ADDRESS", patterns=patterns)
    
class DOBRecognizer(BaseRegexRecognizer):
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

class TitleRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [Pattern("TITLE", r"\b(Mr|Mrs|Ms|Mx|Dr|Prof)\.?\b", score=1.0)]

        super().__init__(supported_entity="TITLE", patterns=patterns)    

class PostNominalRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("POSTNOMINAL", r"\b(PhD|MD|JD|DVM|DDS|CPA|RN|DO|MBBS|BSN|MSN|DNP|NP|CRNA|PA-C|PT|OT|SLP|FACP|FAAFP|FACS|FAAN|DMD|BDS|FAGD|MAGD|ABGD|ABPD|ABOP|ABOMS|ABP|ABO|RDH|EFDA)\b", score=1.0),
            Pattern("POSTNOMINAL", r"\bMS\b", score=0.85)
        ]

        super().__init__(supported_entity="POSTNOMINAL", patterns=patterns)
        
class SSNRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("SSN",r"((\*\*\*\-\*\d\-\d{4})|(\d{3}\-\d{2}\-\d{4}))\b",score=1.0)
        ]
        super().__init__(supported_entity="SSN", patterns=patterns)
    
class MedicaidAccountRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("MEDICAID_ACCOUNT", r"\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b", score=1.0)
        ]
        super().__init__(supported_entity="MEDICAID_ACCOUNT", patterns=patterns)
    
class AllergiesRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("ALLERGIES", r"(?i)allergies:\s*(.*?)\n\s*\n", score=1.0)
            #Pattern("ALLERGIES", r"(?i)allergies:\s*\S((.*\n)*?)(?=.*:)", score=1.0) 
            # Unsuccessful attempt at trying to find a way to identify until a 
            # line ending with a colon is found and exclude that line 
            # form the pattern match (positive look ahead I think)
        ]
        super().__init__(supported_entity="ALLERGIES", patterns=patterns)
    
class LabResultsRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("LAB_RESULTS", r"(?i)lab results[^:]*:\s*(.*?)\n\s*\n", score=1.0)
        ]
        super().__init__(supported_entity="LAB_RESULTS", patterns=patterns)
    
class HospitalRecognizer(BaseRegexRecognizer):
    def __init__(self):
        phrase1 = "Hospital name:"
        phrase2 = "Hospital Name:"
        patterns = [Pattern("HOSPITAL", rf"(?<={re.escape(phrase1)}\s)([^\n]+)|(?<={re.escape(phrase2)}\s)([^\n]+)",score=1.0)]
        super().__init__(supported_entity="HOSPITAL", patterns=patterns)

class FaxRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [Pattern("FAX", r"(?i)"+r"(fax|fax number|fax no.)"+r"\s?:?\s?"+ r"(\+?\d[\d -]{8,}\d)", score=1.0)]
        super().__init__(supported_entity="FAX", patterns=patterns)

class WebURLRecognizer(BaseRegexRecognizer): # Presidio Analzyer has a URL recognizer built-in but this is to avoid false positives (i.e. Ms.Jen being mistaken for ms.***)
    def __init__(self):
        patterns = [Pattern("WEB_URL", r"\b(?:https?://|www\.)[a-zA-Z0-9\-\.]+\.[a-z]{2,}(/[^\s]*)?\b", score=1.0)]
        super().__init__(supported_entity="WEB_URL", patterns=patterns)
    
class NumberRecognizer(BaseRegexRecognizer):
    def __init__(self):
        patterns = [
            Pattern("NUMBER", r"\s?:?\s?"
                    + r"("
                        + r"\d{3}-?\d{4}-?\d{4}|\d{6,9}|"
                        + r"\d{4}\s?\d{4}\s?\d{4}\s?\d{4}|"
                        + r"[A-Z]{2}\d{4}-[A-Z]{3}\d{5}|"
                        + r"[A-Z]\d{4}-\d{7}|[A-Z]{2}\d{3}[a-z]-\d{4}|"
                        + r"[A-Z]\d{4}-\d{7}|[A-Z]{2}\d{3}[a-z]-\d{4}|"
                        + r"[A-Z]\d{4}-\d{7}|[A-Z]{2}\d{3}[a-z]-\d{4}|"
                        + r"[A-Z]{5}-[A-Z][a-z]\d{8}|"
                        + r"[A-Z]{3}\d{4}-[A-Z]{2}\d{5}|"
                        + r"[A-Z]{2}\d{2}-\d{6}"
                    + r")", score=0.75)
        ]
        super().__init__(supported_entity="NUMBER", patterns=patterns)