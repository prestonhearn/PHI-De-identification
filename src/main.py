import os
from Recognizer import AddressRecognizer, DOBRecognizer,TitleRecognizer, PostNominalRecognizer, MedicaidAccountRecognizer
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

file_path = [os.path.join(".", "src", "resources", "ehr JMS.txt"),
             os.path.join(".", "src", "resources", "ehr MH 2.txt")
]

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

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

for file_path in file_path:
    with open(file_path, 'r') as file:
        content = file.read()

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

    final_result_file = os.path.join(".", "src", "RESULTS", f"final_Result_{base_filename}.txt")
    analyzer_file = os.path.join(".", "src", "RESULTS", f"analyzer_{base_filename}.txt")

    # Save anonymized content
    with open(final_result_file, "w") as f:
        f.write(result.text + "\n")

    # Save analysis results
    with open(analyzer_file, "w") as f:
        for result_analyzer in results:
            f.write(str(result_analyzer) + "\n")