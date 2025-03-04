# PHI-De-identification
UTD senior project for professor Salih.


## Virtual Environment and Package Installation Instructions

1. `cd` to the root directory

2. To create virtual environment run:\
    `python -m venv env`
    > **_NOTE:_** Only necessary to do this step once.

3. To activate the virtual environment:\
    On MacOS/Linux run: `source env/bin/activate`\
    On Windows run: `.\env\Scripts\activate`

4. To install the necessary packages run:\
    `pip install -r requirements.txt`

5. If you install any new packages run:\
    `pip freeze > requirements.txt`
    > **_NOTE:_**  If you run this while not in the virtual environment, you will write every package you have ever installed on your local machine to "requirements.txt". Please don't do this