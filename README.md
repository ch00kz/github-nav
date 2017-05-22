Steps: <br><br>

1)  Setup Python 3 virtual environment (developed using python 3.5.1) <br><br>

2)  Install dependencies (located in 'dependencies/requirements.txt'). <br><br>
    From the project's root dir run: `pip install -r dependencies/requirements.txt` <br><br>

3)  Run the application! <br><br>
    From the project's root dir run: `gunicorn application:app` <br><br>

4)  Navigate to http://localhost:8000/navigator?search_term=arrow <br><br>

5)  Note: http://localhost:8000/ or any other route will display the contents of this file.
