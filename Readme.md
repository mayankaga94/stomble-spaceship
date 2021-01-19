Stomble Spaceship

Build (Ubuntu/Linux)

1) Clone repo
2) Create a new python3 virtual environment at top level of project directory
    python3 -m venv env
3) Activate the environment
    source env/bin/activate
4) Install required packages
    pip install -r requirements.txt
5) Run server
    python manage.py runserver

The API is documented at <127.0.0.1:8000/api/docs/> .
To interact with the API, go to the desired url where you can send a POST or PUT request by creating a JSON object in the content box. Similarly a DELETE button is provided to send a DELETE request.