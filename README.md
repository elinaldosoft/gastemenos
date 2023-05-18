### How to install the project
- git clone git@github.com:elinaldosoft/gastemenos.git gastemenos
- cd gastemenos
- python3.11 -m venv venv
- source venv/bin/activate
- poetry install
- python manage.py check
- python manage.py makemigrations
- python manage.py migrate (To create the structure (schemas, tables) the database)

### How to install the project in Windows
- git clone git@github.com:elinaldosoft/gastemenos.git gastemenos
- cd gastemenos
- python -m venv venv
- venv\Scripts\Activate.ps1
- poetry install
- python manage.py check
- python manage.py makemigrations
- python manage.py migrate (To create the structure (schemas, tables) the database)

### Running project
- python manage.py runserver
- http://127.0.0.1:8000/

### Python
- https://www.python.org/downloads/

### Poetry
- https://python-poetry.org/docs
- Use the version Poetry (version 1.3.2)

### Create user to admin and access dashboard
- python manage.py createsuperuser
- http://127.0.0.1:8000/admin

### How to install the project in Windows
- git clone git@github.com:elinaldosoft/gastemenos.git gastemenos
- cd gastemenos
- python -m venv venv
- venv\Scripts\Activate.ps1
- poetry install
- python manage.py check
- python manage.py migrate (To create the structure (schemas, tables) the database)