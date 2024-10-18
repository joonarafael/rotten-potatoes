# Rotten Potatoes

Movie rating website built as a university assignment for course "Tietokannat ja web-ohjelmointi". All features are implemented as required by the initial software requirements specification (below).

## Updates

**Oct 18, 2024**: All features described in this document are implemented & working as intended.

## Technical Overview

Application is built with _Python Flask_ framework. Database is _PostgreSQL_ (run as a _Docker_ container).

## Installation Manual

Installation Manual can be found [here](./docs/installation_manual.md "Installation Manual").

## Project Description

The application is a simple and limited movie rating website. User can register and login, add new movies and rate them (their own and others). Rating consists of a star rating from 1-10 and a free-form comment. When adding a movie, user must provide the movie title, category (e.g. comedy, drama, action, etc.), description and release year.

User can also delete their own ratings. User cannot delete their own movie, **if someone else has rated it**. User can also view other users' ratings and movies. Movies can be searched by title and filtered by category.

The application also has superusers (no registration possibility, added during database creation), who can (in addition to all the features of a regular user) delete any movies and ratings. Superusers can also change the details of any movie.

## Admin Users

Pre-populated superusers:

```
alice:redqueen
bob:squarepants
patrick:asteroid
```

## Pylint Style Check

Run the bash script named `./pylint.sh` to check the style of the Python code. You might need to grant execution rights first with `chmod u+x pylint.sh`.

Read the bash script contents with `cat pylint.sh` - never execute scripts you don't trust!
