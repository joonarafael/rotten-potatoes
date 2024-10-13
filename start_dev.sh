# script to start the development environment

code .
cd db
docker compose up -d
cd ..
source ./venv/bin/activate
cd src
flask run --reload