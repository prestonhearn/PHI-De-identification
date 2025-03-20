import os
from Recognizer import AddressRecognizer, DOBRecognizer, TitleRecognizer, PostNominalRecognizer
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = os.path.join(".", "src", "resources", "ehr JMS.txt")

#"./resources/ehr JMS.txt"
with open(file_path, 'r') as file:
    content = file.read()

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

address_rec = AddressRecognizer()
dob_rec = DOBRecognizer()
title_rec = TitleRecognizer() 
postnominal_rec = PostNominalRecognizer()



analyzer.registry.add_recognizer(address_rec)
analyzer.registry.add_recognizer(dob_rec)
analyzer.registry.add_recognizer(title_rec)
analyzer.registry.add_recognizer(postnominal_rec)

results = analyzer.analyze(text=content,
                           entities=["PERSON", "ADDRESS", "DOB", "US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS", "TITLE", "POSTNOMINAL"],
                           language='en')

result = anonymizer.anonymize(
    text=content,
    analyzer_results=results,
    operators={"PERSON": OperatorConfig("replace", {"new_value": "*name*"}),
               "ADDRESS": OperatorConfig("replace", {"new_value": "*address*"}),
               "TITLE": OperatorConfig("replace",  {"new_value": "*title*"}),
               "DOB": OperatorConfig("replace", {"new_value": ("\nDate of Birth: " + "*dob*")}),
               "US_SSN": OperatorConfig("replace", {"new_value": "*ssn*"}), 
               "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "*phone*"}), 
               "POSTNOMINAL": OperatorConfig("replace", {"new_value": "*pn*"}), 
               "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "*email*"})},

)

file_Result_File = os.path.join(".", "src", "resources", "final_Result.txt")
with open(file_Result_File, "w") as f:
    f.write(result.text + "\n")

file_Analyzer_File = os.path.join(".", "src", "resources", "analyzer_File.txt")
with open(file_Analyzer_File, "w") as f:
    for result_analyzer in results:
        f.write(str(result_analyzer) + "\n")