# PHI De-Identification Tool

A graphical application for detecting, anonymizing, and re-identifying Protected Health Information (PHI) in plain text files.

This tool was developed as part of a senior project at the University of Texas at Dallas for Professor Salih.

---

## 📌 Overview

This app uses [Microsoft Presidio](https://github.com/microsoft/presidio) and custom recognizers to:
- Identify sensitive entities (e.g., SSNs, addresses, DOBs, etc.) in text.
- Encrypt selected entities using a provided key.
- Save anonymized files and associated metadata.
- Re-identify entities using stored metadata and the same key.

The user interface is built with Python’s Tkinter library for easy file selection and operation.

---

## 🛠 Setup Instructions

1. Clone the repository and `cd` into the root directory.

2. **Create a virtual environment** (only needed once):

    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment**:

    - On **Windows**:
      ```bash
      .\env\Scripts\activate
      ```

    - On **macOS/Linux**:
      ```bash
      source env/bin/activate
      ```

4. **Install required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. If you add new packages later:

    ```bash
    pip freeze > requirements.txt
    ```

    > ⚠️ **Important:** Only do this inside the virtual environment, or you'll capture system-wide packages by mistake.

---

## 🚀 Running the App

Once the environment is set up and activated:

```bash
python ./src/PHI-De-Identification.py
