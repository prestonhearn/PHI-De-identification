import os
from Recognizer import Address
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = os.path.join(".", "src", "resources", "ehr JMS.txt")

#"./resources/ehr JMS.txt"
with open(file_path, 'r') as file:
    content = file.read()

analyzer = AnalyzerEngine()
engine = AnonymizerEngine()

custom_recognizer = Address()
analyzer.registry.add_recognizer(custom_recognizer)

results = analyzer.analyze(text=content,
                           entities=["PERSON", "ADDRESS", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS"],
                           language='en')

result = engine.anonymize(
    text=content,
    analyzer_results=results,
    operators={"PERSON": OperatorConfig("replace"),
               "ADDRESS": OperatorConfig("replace"),
               "US_SSN": OperatorConfig("replace"), 
               "PHONE_NUMBER": OperatorConfig("replace"), 
               "EMAIL_ADDRESS": OperatorConfig("replace")},
)

print(result)
