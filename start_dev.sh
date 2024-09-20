# script to start the development environment

cd db
docker compose up -d
cd ..
source ./venv/bin/activate
cd src
flask run --reload