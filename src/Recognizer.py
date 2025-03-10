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
        
        # Your custom logic to identify entities
        for match in re.finditer(self.patterns, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity_type": "ADDRESS",
                "score": 1.0,
            })
        
        return matches
