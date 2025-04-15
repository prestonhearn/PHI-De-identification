import os
from Recognizer import (
    AddressRecognizer,
    DOBRecognizer,
    TitleRecognizer,
    PostNominalRecognizer,
    SSNRecognizer,
    MedicaidAccountRecognizer,
    AllergiesRecognizer,
    LabResultsRecognizer,
    HospitalRecognizer,
    FaxRecognizer,
    WebURLRecognizer,
    MedicalRecordNumberRecognizer,
    HealthPlanBeneficiaryNumberRecognizer,
    PacemakerSerialNumberRecognizer
)
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

ehr3_filepath = os.path.join(".", "src", "resources", "ehr EC 3 .txt")
file_path = [os.path.join(".", "src", "resources", "ehr JMS.txt"),
             os.path.join(".", "src", "resources", "ehr MH 2.txt"),
             ehr3_filepath
]

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

recognizers = [
    AddressRecognizer(),
    DOBRecognizer(),
    TitleRecognizer(),
    PostNominalRecognizer(),
    SSNRecognizer(),
    MedicaidAccountRecognizer(),
    AllergiesRecognizer(),
    LabResultsRecognizer(),
    HospitalRecognizer(),
    FaxRecognizer(),
    WebURLRecognizer(),
    MedicalRecordNumberRecognizer(),
    HealthPlanBeneficiaryNumberRecognizer(),
    PacemakerSerialNumberRecognizer()
]

for recognizer in recognizers:
    analyzer.registry.add_recognizer(recognizer)

for file_path in file_path:
    with open(file_path, 'r') as file:
        content = file.read()
    
    if file_path == ehr3_filepath:
        entities = [
            "TITLE", "PERSON", "POSTNOMINAL", "ADDRESS", "DOB",
            "DATE_TIME", "PHONE_NUMBER", "FAX", "EMAIL_ADDRESS",
            "SSN",  "MEDICAID_ACCOUNT", "WEB_URL", "IP_ADDRESS",
            "MED_REC_NUM", "HPBN", "PSN"
        ]
    else:
        entities = [
            "PERSON", "ADDRESS", "DOB", "SSN", "PHONE_NUMBER", 
            "EMAIL_ADDRESS", "TITLE", "POSTNOMINAL", "MEDICAID_ACCOUNT",
            "ALLERGIES", "LAB_RESULTS", "HOSPITAL", "IP_ADDRESS", 
            "MED_REC_NUM", "HPBN", "PSN"
        ]

    operator_config = {
        "TITLE": OperatorConfig("replace", {"new_value": "*title*"}),
        "PERSON": OperatorConfig("replace", {"new_value": "*name*"}),
        "POSTNOMINAL": OperatorConfig("replace", {"new_value": "*pn*"}),            
        "ADDRESS": OperatorConfig("replace", {"new_value": "*address*"}),
        "DATE_TIME": OperatorConfig("replace", {"new_value": "*date*"}),
        "DOB": OperatorConfig("replace", {"new_value": "\nDate of Birth: *dob*"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "*phone*"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "*email*"}),
        "SSN": OperatorConfig("replace", {"new_value": "*ssn*"}),
        "MEDICAID_ACCOUNT": OperatorConfig("replace", {"new_value": "*medicaid*"}),
        "ALLERGIES": OperatorConfig("replace", {"new_value": "*allergies*\n\n"}),
        "LAB_RESULTS": OperatorConfig("replace", {"new_value": "*lab results*\n\n"}),
        "HOSPITAL": OperatorConfig("replace", {"new_value": "*hospital*"}),
        "FAX": OperatorConfig("replace", {"new_value": "*fax*"}),
        "WEB_URL": OperatorConfig("replace", {"new_value": "*url*"}),
        "IP_ADDRESS": OperatorConfig("replace", {"new_value": "*ip*"}),
        "MED_REC_NUM": OperatorConfig("replace", {"new_value": "*med_rec_num*"}),
        "HPBN": OperatorConfig("replace", {"new_value": "*hpbn*"}),
        "PSN": OperatorConfig("replace", {"new_value": "*psn*"})
    }
    

    results = analyzer.analyze(
        text=content,
        entities=entities,
        language='en'
    )

    result = anonymizer.anonymize(
        text=content,
        analyzer_results=results,
        operators=operator_config
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