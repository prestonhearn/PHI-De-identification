import os
from Recognizer import AddressRecognizer, DOBRecognizer,TitleRecognizer, PostNominalRecognizer, MedicaidAccountRecognizer
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
title_rec = TitleRecognizer() 
postnominal_rec = PostNominalRecognizer()
medicaid_rec = MedicaidAccountRecognizer()



analyzer.registry.add_recognizer(address_rec)
analyzer.registry.add_recognizer(dob_rec)
analyzer.registry.add_recognizer(title_rec)
analyzer.registry.add_recognizer(postnominal_rec)
analyzer.registry.add_recognizer(medicaid_rec)

results = analyzer.analyze(text=content,
                           entities=["PERSON", "ADDRESS", "DOB", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS", "TITLE", "POSTNOMINAL", "MEDICAID_ACCOUNT"],
                           language='en')

result = engine.anonymize(
    text=content,
    analyzer_results=results,

    operators={"PERSON": OperatorConfig("replace"),
               "ADDRESS": OperatorConfig("replace"),
               "TITLE": OperatorConfig("replace"),
               "DOB": OperatorConfig("replace", {"new_value": "\nDate of Birth: <DOB>"}),
               "US_SSN": OperatorConfig("replace"), 
               "PHONE_NUMBER": OperatorConfig("replace"),
               "POSTNOMINAL": OperatorConfig("replace"), 
               "EMAIL_ADDRESS": OperatorConfig("replace"),
               "MEDICAID_ACCOUNT": OperatorConfig("replace")},
)

file_Result_File = os.path.join(".", "src", "resources", "final_Result.txt")
with open(file_Result_File, "w") as f:
    f.write(result.text + "\n")

