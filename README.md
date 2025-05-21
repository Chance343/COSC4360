This project is a document processing pipeline developed as a senior project. It uses OCR and natural language processing to extract structured data from PDFs and images, with a frontend for drag-and-drop file uploads, a backend API that processes files with OpenAI's GPT-4 Vision model, and a PostgreSQL database to store results.

My Contributions:
- Collaborated on planning and testing the backend API.
- Assisted in data structuring and integrating NLP results.
- Supported frontend-backend communication through API endpoints.

Technologies Used:
- Python (FastAPI, OpenAI API)
- JavaScript (React for frontend)
- PostgreSQL
- EasyOCR and the NLP model spaCy

You need to be running the backend to be able to upload the file to the backend



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
    
    Configure ENV:
        Open backend_openAI folder in Editor
        create '.env' file with OPENAI_API_KEY=<api_key>

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

Database (only requires configuration)
    
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

    Once complete run "uvicorn main:app --reload" to reload backend
