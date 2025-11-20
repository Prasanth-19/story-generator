@echo off
REM Activate the virtual environment (same folder)
call myenv\Scripts\activate

REM Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

REM Run Flask app
flask run

pause
