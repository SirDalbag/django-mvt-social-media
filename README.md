# TwiiterX
Social media on Django MVT

## Key Features:
* User registration and authorization, ability to edit profile
* Creating, editing and deleting posts, ability to leave reactions and comments
* Post feed, ability to follow other users

## Technology Stack:
* Django (MVT)
* ORM 
* HTML, CSS (Tailwind) and JavaScript

## Getting Started:
1. Clone the repository: `https://github.com/SirDalbag/django-mvt-social-media.git`
2. Create and start the virtual environment: `python -m venv venv`, `call venv/scripts/activate`
    * If an error occurs when starting the virtual environment:
        1. Open <font color="red">PowerShell</font> as **administrator**
        2. Execute the command: `Set-ExecutionPolicy RemoteSigned`
        3. To the question - <font color="green">**A**</font>
3. Install dependencies: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`
---
## License:
This project is licensed under the terms of the [MIT License](https://github.com/SirDalbag/django-mvt-social-media/blob/main/LICENSE).