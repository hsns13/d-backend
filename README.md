# Virtual Environments (virtualenv)
    to isolate dependencies per project install pipenv
    - pip3 install pipenv
    - pipenv --three | python3 virtual env for the project
    - pipenv install flask | install flask as a dependency on the project

# Notes 
- to make things concise I chose to use list as a data structure on the rest api
- if needed I can add persistent data storage

# Data storage
- just to make the application run I'm holding state of the application in the list

# Dockerfile
# Run Docker container
    to build the image with the tag name todo
    - docker build -t todo .

    run a new docker container which is named todo
    - docker run --name todo -d -p 5000:5000 todo

# Without docker
    to run the flask app without docker

    file content of bootstrap.sh could be changed with the custom port number or any other prefered port number instead of listening all interfaces ( 0.0.0.0 )

    #!/bin/sh
    export FLASK_APP=./todo/index.py
    source $(pipenv --venv)/bin/activate
    flask run -h localhost -p 3013

    Then ofcourse if 3013 as a port number is choosed then on the react/client .env file should be updated to localhost:3013

# Test
- run the server
    on the command window run ./bootstrap.sh
- run the test
    pipenv run pytest -vv