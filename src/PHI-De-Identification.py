import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
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
    NumberRecognizer
)
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.entities import OperatorConfig, OperatorResult

# Init Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
deanonymizer = DeanonymizeEngine()

default_key = "0123456789abcdef"

ENTITY_LIST = [
    "TITLE", "PERSON", "POSTNOMINAL", "ADDRESS", "DOB",
    "DATE_TIME", "PHONE_NUMBER", "FAX", "EMAIL_ADDRESS",
    "SSN",  "MEDICAID_ACCOUNT", "ALLERGIES", "LAB_RESULTS",
    "HOSPITAL", "WEB_URL", "IP_ADDRESS", "NUMBER"
]

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
    NumberRecognizer()
]

for recognizer in recognizers:
    analyzer.registry.add_recognizer(recognizer)

class DeIdentificationUI:
    def __init__(self, root):
        self.root = root
        root.title("PHI De-Identification App")

        self.file_label = ttk.Label(root, text="No file selected")
        self.file_label.pack(pady=5)

        self.browse_btn = ttk.Button(root, text="Browse File", command=self.select_file)
        self.browse_btn.pack(pady=5)

        # Entity selection
        self.entity_vars = {ent: tk.BooleanVar() for ent in ENTITY_LIST}
        self.entity_frame = ttk.LabelFrame(root, text="Entities to De-Identify")
        self.entity_frame.pack(pady=10, padx=10, fill="x")

        for i, ent in enumerate(ENTITY_LIST):
            cb = ttk.Checkbutton(self.entity_frame, text=ent, variable=self.entity_vars[ent])
            cb.grid(row=i // 3, column=i % 3, sticky='w', padx=5, pady=2)

        # Encryption key
        self.key_label = ttk.Label(root, text="Encryption/Decryption Key:")
        self.key_label.pack()
        self.key_entry = ttk.Entry(root, width=50)
        self.key_entry.insert(0, default_key)
        self.key_entry.pack(pady=5)

        # Action buttons
        self.anonymize_btn = ttk.Button(root, text="Anonymize", command=self.anonymize_file)
        self.anonymize_btn.pack(pady=5)

        self.deanonymize_btn = ttk.Button(root, text="Deanonymize", command=self.deanonymize_file)
        self.deanonymize_btn.pack(pady=5)

        # Status
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.selected_file = None

    
    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.selected_file = filepath
            self.file_label.config(text=os.path.basename(filepath))

    def anonymize_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected.")
            return

        with open(self.selected_file, "r", encoding="utf-8") as f:
            text = f.read()

        entities = [ent for ent, var in self.entity_vars.items() if var.get()]
        if not entities:
            messagebox.showwarning("Warning", "No entities selected.")
            return

        results = analyzer.analyze(text=text, entities=entities, language="en")

        key = self.key_entry.get()
        operators = {
            ent: OperatorConfig("encrypt", {"key": key}) 
            for ent in entities
        }

        result = anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )

        output_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")],
                                                   title="Save Anonymized File")
        if output_path:
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(result.text)

            metadata_path = output_path + ".meta.json"
            with open(metadata_path, "w", encoding="utf-8") as meta_out:
                json.dump([item.to_dict() for item in result.items], meta_out)

            self.status_label.config(text=f"Anonymized file saved: {os.path.basename(output_path)}")

    def deanonymize_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        meta_path = filepath + ".meta.json"
        if not os.path.exists(meta_path):
            messagebox.showerror("Missing Metadata", "No metadata file found for this anonymized text.")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            anon_text = f.read()

        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        operator_results = [
            OperatorResult(
                start=item["start"],
                end=item["end"],
                entity_type=item["entity_type"],
                operator=item["operator"],
                text=item["text"]
            ) for item in metadata
        ]

        key = self.key_entry.get()

        result = deanonymizer.deanonymize(
            text=anon_text,
            operators={"DEFAULT": OperatorConfig("decrypt", {"key": key})},
            entities=operator_results,
        )

        output_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")],
                                                title="Save Deanonymized File")
        if output_path:
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(result.text)
            self.status_label.config(text=f"Deanonymized file saved: {os.path.basename(output_path)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DeIdentificationUI(root)
    root.mainloop()