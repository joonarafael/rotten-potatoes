# INSTALLATION MANUAL

Written in English for accessibility.

This installation manual will guide you through the process of setting up the development environment for the _Rotten Potatoes_ application. The application is built with _Python_ and _Flask_, and it uses _PostgreSQL_ as the database.

Instructions are written for a Linux environment, but the process should be similar on other operating systems as well.

## Docker & PostgreSQL

Make sure you are not in any virtual environment while running the following commands. If you are, deactivate the virtual environment.

This software requires you to run the database as a _Docker_ container. The database won't work natively through the `psql` command.

### Docker Compose

Make sure to have _Docker Compose_ installed on your machine. If you don't have it installed, you can follow the instructions [here](https://docs.docker.com/compose/install/ "Overview of installing Docker Compose").

Check a successful installation by running the following command:

```bash
docker compose version
```

**NOTE!** Some machines & setups might use `docker-compose` instead of `docker compose` (depends on the method of installation (Docker Engine / Docker Desktop, etc.)). If you encounter an error, try using `docker-compose` instead.

**OPTIONAL:** Before launching the DB, you can alter the available genres in the database by modifying the `./init-db.sh` file! The file contains the initial setup for the database, including the superusers & available genres. Genres start from line 86. **However, be careful not to break anything**!

**Launching the DB Container**

Once you've got _Docker Compose_ installed, you can launch the PostgreSQL container by executing the following command

```bash
docker compose up
```

in the [`./db`](../db/) directory. This will launch the PostgreSQL container with the necessary configurations.

To stop & remove the container, execute the following command (in the [`./db`](../db/) directory):

```bash
docker compose down
```

**NOTE!** I've not defined any volumes for the DB, so the data will be lost when the container is removed. If you'd like to persist the data, you should configure a volume in the `docker-compose.yml` file.

## Useful Docker Commands

- Check all your Docker containers with `docker ps -a` and all images with `docker images`.
- List all Docker networks with `docker network ls`.
- Any container can be first stopped with `docker stop {container}` and then deleted with `docker rm {container}`.
- All images can be listed with `docker images`.
- Any image can be deleted wih `docker rmi {image:version}`.
- Any Docker network can be deleted with `docker network rm {network}`.

## Defining Environment Variables

Create a `.env` file in the [`./src`](../src/ "../src") directory of the project and define the following environment variables:

```bash
SQLALCHEMY_DATABASE_URI = 'URL_TO_YOUR_DATABASE'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '***'
```

**Define the** `SECRET_KEY` **as you wish**. It is used for securing the session data. Do not change it after initial setup, as it will invalidate all existing sessions.

Adjust the `SQLALCHEMY_DATABASE_URI` to connect to the database. If you are using the default database setup with Docker Compose, as described above, you can use the following URI:

```bash
postgresql://postgres:postgres@localhost:1234/rottenpotatoes
```

These keys (in version control) are intended for local development environments & testing only. If moving to production, make sure to change the credentials and use a more secure method for storing sensitive information.

## Python & Python Virtual Environment

### Version

**This software was built using Python version 3.10.12**. Software will likely run on other versions as well, but if you begin to encounter issues, consider installing Python 3.10.12.

**NOTE!** A virtual environment can be initialized with a specific Python version as long as the version binary is available on the system.

Other options include global installation, as well as the managing of multiple Python versions (and specific Python versions within specific directories) with a dedicated tool, like [pyenv](https://github.com/pyenv/pyenv "Simple Python Version Management: pyenv").

You can check your Python version with the following command:

```bash
python3 -V
```

### Virtual Environment

Create a new _Python virtual environment_ by executing the following command in the repository root (e.g. [here](.. "Rotten Potatoes")):

```bash
python3 -m venv venv
```

To activate the virtual environment, use the following command (in the repo root (again) or adjust the path accordingly):

```bash
source ./venv/bin/activate
```

To deactivate the virtual environment, use the following command (this can be done from anywhere):

```bash
deactivate
```

## Install Dependencies

**After activating the virtual environment**, install the required dependencies by executing the following command in the [repository root](.. "Rotten Potatoes"):

```bash
pip install -r requirements.txt
```

## Running the Application

You are set. Enter the Python virtual environment (if you haven't already) and **enter the [`./src`](../src/ "./src") directory**. To start the application, run the following command:

```bash
flask run
```

The application will be running on [`localhost:5000`](http://127.0.0.1:5000 "localhost:5000") as a default, but Flask will provide you with the exact URL in any case.
