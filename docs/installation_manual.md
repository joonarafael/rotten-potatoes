# INSTALLATION MANUAL

## Docker & PostgreSQL

Make sure you are not in any virtual environment while running the following commands. If you are, deactivate the virtual environment.

This software requires you to run the database as a _Docker_ container. If you are comfortable with running `psql` natively on your machine, you can do that as well. But I'm not. So, I'll be using Docker to run the PostgreSQL container.

If you choose to run the database natively, you can find the database schema in the [`./db`](../db/) directory. You can create the database and tables by running the SQL scripts in the `schema.sql` file.

**Docker Compose**

Make sure to have _Docker Compose_ installed on your machine. If you don't have it installed, you can follow the instructions [here](https://docs.docker.com/compose/install/ "Overview of installing Docker Compose").

**Launching the DB Container**

Once you've got _Docker Compose_ installed, you can launch the PostgreSQL container by executing the following command

```bash
docker compose up
```

in the [`./db`](../db/) directory. This will launch the PostgreSQL container with the necessary configurations. Some machines & setups might use `docker-compose` instead of `docker compose`. If you encounter an error, try using `docker-compose` instead.

To stop & remove the container, execute the following command:

```bash
docker compose down
```

## Useful Docker Commands

- Check all your Docker containers with `docker ps -a` and all images with `docker images`.
- List all Docker networks with `docker network ls`.
- Any container can be first stopped with `docker stop {container}` and then deleted with `docker rm {container}`.
- Any image can be deleted wih `docker rmi {image:version}`.
- Any Docker network can be deleted with `docker network rm {network}`.

## Defining Environment Variables

Create a `.env` file in the [`./src`](../src/) directory of the project and define the following environment variables:

```bash
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:1234/rottenpotatoes'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'secret'
```

## Python & Python Virtual Environment

**This software was built using Python version 3.10.12**. Software will likely run on other versions as well, but if you begin to encounter issues, consider installing Python 3.10.12. If you've got the Python version binaries downloaded, you can initialize the virtual environment to use the correct Python version.

Other options include global installation, as well as the managing of multiple Python versions (and specific Python versions within specific directories) with a dedicated tool, like [pyenv](https://github.com/pyenv/pyenv "Simple Python Version Management: pyenv").

You can check your Python version with the following command:

```bash
python3 -V
```

Create a new _Python virtual environment_ with the following command:

```bash
python3 -m venv venv
```

The command might differ depending on your operating system. The above command is for _Linux_. Consult [this documen](https://docs.python.org/3/library/venv.html "Python venv — Creation of virtual environments") to find the correct command for your operating system.

To activate the virtual environment, use the following command:

```bash
source venv/bin/activate
```

To deactivate the virtual environment, use the following command:

```bash
deactivate
```

## Install Dependencies

**After activating the virtual environment**, install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

You are set. Enter the Python virtual environment (if you haven't already) and run the application by executing

```bash
flask run
```

in the [`./src`](../src/) directory. The application will be running on [`localhost:5000`](http://127.0.0.1:5000 "localhost:5000").
