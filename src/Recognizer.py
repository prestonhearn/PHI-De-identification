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


