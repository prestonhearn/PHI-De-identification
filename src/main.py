import os
from Recognizer import AddressRecognizer, DOBRecognizer, TitleRecognizer, PostNominalRecognizer, SSNRecognizer, MedicaidAccountRecognizer, HospitalRecognizer
from presidio_analyzer import AnalyzerEngine
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
ssn_rec = SSNRecognizer()
medicaid_rec = MedicaidAccountRecognizer()
hospital_rec = HospitalRecognizer()  


analyzer.registry.add_recognizer(address_rec)
analyzer.registry.add_recognizer(dob_rec)
analyzer.registry.add_recognizer(title_rec)
analyzer.registry.add_recognizer(postnominal_rec)
analyzer.registry.add_recognizer(ssn_rec)
analyzer.registry.add_recognizer(medicaid_rec)
analyzer.registry.add_recognizer(hospital_rec)

#"./resources/ehr JMS.txt"

for file_path in file_path:
    with open(file_path, 'r') as file:
        content = file.read()

    results = analyzer.analyze(text=content,
                            entities=["PERSON", "ADDRESS", "DOB", "SSN", "PHONE_NUMBER", "EMAIL_ADDRESS", "TITLE", "POSTNOMINAL", "MEDICAID_ACCOUNT", "HOSPITAL"],
                            language='en')

    result = anonymizer.anonymize(
        text=content,
        analyzer_results=results,
        operators={"PERSON": OperatorConfig("replace", {"new_value": "*name*"}),
                "ADDRESS": OperatorConfig("replace", {"new_value": "*address*"}),
                "TITLE": OperatorConfig("replace",  {"new_value": "*title*"}),
                "DOB": OperatorConfig("replace", {"new_value": ("\nDate of Birth: " + "*dob*")}),
                "SSN": OperatorConfig("replace", {"new_value": "*ssn*"}), 
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "*phone*"}), 
                "POSTNOMINAL": OperatorConfig("replace", {"new_value": "*pn*"}), 
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "*email*"}),
                "MEDICAID_ACCOUNT": OperatorConfig("replace", {"new_value": "*medicaid*"}),
                "HOSPITAL": OperatorConfig("replace", {"new_value": "*hospital*"})
                }

    )
    # Generate unique filenames for each processed file
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    final_result_file = os.path.join(".", "src", "RESULTS", f"final_Result_{base_filename}.txt")
    analyzer_file = os.path.join(".", "src", "RESULTS", f"analyzer_{base_filename}.txt")

    # Save anonymized content
    with open(final_result_file, "w") as f:
        f.write(result.text + "\n")

    # Save analysis results
    with open(analyzer_file, "w") as f:
        for result_analyzer in results:
            f.write(str(result_analyzer) + "\n")