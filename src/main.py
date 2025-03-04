import os
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = os.path.join(".", "src", "resources", "ehr JMS.txt")

#"./resources/ehr JMS.txt"
with open(file_path, 'r') as file:
    content = file.read()

analyzer = AnalyzerEngine()
engine = AnonymizerEngine()

results = analyzer.analyze(text=content,
                           entities=["PERSON", "LOCATION", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS"],
                           language='en')

result = engine.anonymize(
    text=content,
    analyzer_results=results,
    operators={"PERSON": OperatorConfig("redact"),
               "LOCATION": OperatorConfig("redact"), 
               "US_SSN": OperatorConfig("redact"), 
               "PHONE_NUMBER": OperatorConfig("redact"), 
               "EMAIL_ADDRESS": OperatorConfig("redact")},
)

print(result)
