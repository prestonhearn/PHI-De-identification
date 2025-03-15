from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern
import re

class AddressRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("ADDRESS", r"\d{1,5}\s([A-Za-z0-9#,.&'-]+\s)+(?:\s(?:Apt|Suite|Unit|#)\s?\d+[a-zA-Z]?,?)?"
                            + r"\s?[a-zA-Z]?,?\s?[a-zA-Z]{2}\s\d{5}", score=1.0)]

        super().__init__(supported_entity="ADDRESS", patterns=patterns)

    def find(self, text, entities=None):
        matches = []
        
        for match in re.finditer(self.patterns, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": "ADDRESS",
                "score": 1.0,
            })
            
        return matches
    
class DOBRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("DOB", r"(?i)(date of birth|dob)\s?:?\s?(\d{2}/\d{2}/\d{4})", score=1.0)]

        super().__init__(supported_entity="DOB", patterns=patterns)

    def find(self, text, entities=None):
        matches = []

        for match in re.finditer(self.patterns, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": "DOB",
                "score": 1.0,
            })

        return matches

class TitleRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("TITLE", r"\b(Mr|Mrs|Ms|Mx|Dr|Prof)\.?\b", score=1.0)]

        super().__init__(supported_entity="TITLE", patterns=patterns)
    
    def find(self, text, entities=None):
        matches = []

        for match in re.finditer(self.patterns, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": "TITLE",
                "score": 1.0,
            })

        return matches

class PostNominalRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [Pattern("POSTNOMINAL", r"\b(PhD|MD|JD|DVM|DDS|CPA|RN)\b", score=1.0)]

        super().__init__(supported_entity="POSTNOMINAL", patterns=patterns)

    def find(self, text, entities=None):
        matches = []

        for match in re.finditer(self.patterns, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": "POSTNOMINAL",
                "score": 1.0,
            })

        return matches

        