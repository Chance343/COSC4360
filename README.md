You need to be running the backend to be able to uplaod the file to the backend



Frontend
    Start program:
        cd frontend/drag-and-drop-test

        DO THIS ONLY FIRST TIME:
        {
            npm install
        }

        npm start



Make a Python virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip3 freeze > requirements.txt (anytime you want to update the dependencies)

Backend (need a separate terminal)
    Activate API:
        cd backend_openAI

        DO THIS ONLY FIRST TIME:
        {
            python3 -m venv venv (i)
            source venv/bin/activate
            pip install -r requirements.txt
        }
        OTHER TIMES
        {
            source venv/bin/activate
        }

        uvicorn main:app --reload

Database (need a separate terminal)
    
    Install PostgreSQL:

        PostgreSQL Installer Link - https://www.postgresql.org/download/
        pgAdmin 4 Installer Link - https://www.pgadmin.org/download/

    Configure Database (using pgAdmin 4):
        1. Open pgAdmin 4
        2. Go to Servers -> PostgreSQL 17 -> Databases
        3. Right-click Databases to create new database
        4. Enter DB name (to be saved for further backend configuration)

    Configure Application connection to Database:
        1. open backend_openAI/db.py in Editor
        2. edit the db configurations:
            a. db_host = "localhost"
            b. db_name = <name given during database configuration>
            c. db_user = <user name>
            d. db_password = <user password>
