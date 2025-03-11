import os
from Recognizer import AddressRecognizer, DOBRecognizer
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = os.path.join("." , "src", "resources", "ehr JMS.txt")

#"./resources/ehr JMS.txt"
with open(file_path, 'r') as file:
    content = file.read()

analyzer = AnalyzerEngine()
engine = AnonymizerEngine()

address_rec = AddressRecognizer()
dob_rec = DOBRecognizer()
analyzer.registry.add_recognizer(address_rec)
analyzer.registry.add_recognizer(dob_rec)

results = analyzer.analyze(text=content,
                           entities=["PERSON", "ADDRESS", "DOB", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS"],
                           language='en')

result = engine.anonymize(
    text=content,
    analyzer_results=results,
    operators={"PERSON": OperatorConfig("replace", {"new_value": "*" * len(results)}),
               "ADDRESS": OperatorConfig("replace", {"new_value": "*" * len(results)}),
               "DOB": OperatorConfig("replace", {"new_value": "\nDate of Birth: <DOB>"}),
               "US_SSN": OperatorConfig("replace", {"new_value": "*" * len(results)}), 
               "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "*" * len(results)}), 
               "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "*" * len(results)})},

)

with open("final_Result.txt", "w") as f:
    f.write(result.text + "\n")

