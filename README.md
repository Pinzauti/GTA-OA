# GTA OA
[![Tests](https://github.com/Pinzauti/GTA-OA/actions/workflows/python-app.yml/badge.svg)](https://github.com/Pinzauti/GTA-OA/actions/workflows/python-app.yml)
[![Pylint](https://github.com/Pinzauti/GTA-OA/actions/workflows/pylint.yml/badge.svg)](https://github.com/Pinzauti/GTA-OA/actions/workflows/pylint.yml)

GUI Technologies & Applications Online Assessment
## File structure

    .
    ├── .github                     # Github actions
    ├── resources/                  # Contains the resources needed for the program.
    │   └── test.json               # Contains the test data for the program.
    ├── src/
    │   ├── .env                    # Environment variables.
    │   ├── exceptions_main.py      # Exceptions of program.
    │   ├── main.py                 # Entrypoint of the program, you should run this.
    │   ├── requirements.txt        # Contains the packages needed to run the program.
    │   └── test_main.py            # Contains the tests for the program.
    ├── .gitignore                  # Contains the files that should be ignored by git.
    ├── .pylintrc                   # Contains the configuration for pylint.
    └── README.md                   # This file.
## Getting started

Execute:
```
cd src/
pip install -r requirements.txt
python main.py
```

Test:
```
 python -m pytest
```



