import os
from Recognizer import AddressRecognizer, DOBRecognizer, PNRecognizer
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = os.path.join(".", "src", "resources", "ehr JMS.txt")

#"./resources/ehr JMS.txt"
with open(file_path, 'r') as file:
    content = file.read()

analyzer = AnalyzerEngine()
engine = AnonymizerEngine()

address_rec = AddressRecognizer()
dob_rec = DOBRecognizer()
pn_rec = PNRecognizer()
analyzer.registry.add_recognizer(address_rec)
analyzer.registry.add_recognizer(dob_rec)
analyzer.registry.add_recognizer(pn_rec)

results = analyzer.analyze(text=content,
                           entities=["PERSON", "ADDRESS", "DOB", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS", "POST-NOMINAL"],
                           language='en')

result = engine.anonymize(
    text=content,
    analyzer_results=results,
    operators={"PERSON": OperatorConfig("replace", {"new_value": "*" * 6}),
               "ADDRESS": OperatorConfig("replace", {"new_value": "*" * 6}),
               "DOB": OperatorConfig("replace", {"new_value": ("\nDate of Birth: " + "*" * 6)}),
               "US_SSN": OperatorConfig("replace", {"new_value": "*" * 6}), 
               "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "*" * 6}), 
               "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "*" * 6}),
               "POST-NOMINAL": OperatorConfig("replace", {"new_value": "*" * 6})}
)

file_Result_File = os.path.join(".", "src", "resources", "final_Result.txt")
with open(file_Result_File, "w") as f:
    f.write(result.text + "\n")

