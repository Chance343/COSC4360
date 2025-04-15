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
        cd backend

        DO THIS ONLY FIRST TIME:
        {
            python3 -m venv venv (i)
            source venv/bin/activate
            pip install -r requirements.txt
        }

        uvicorn main:app --reload