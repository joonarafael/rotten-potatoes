# Rotten Potatoes

Movie rating website built as a university assignment for course "Tietokannat ja web-ohjelmointi". All features are implemented as required by the initial software requirements specification (below).

## Technical Overview

Application is built with _Python Flask_ framework. Database is _PostgreSQL_ (run as a _Docker_ container).

## Installation Manual

Installation Manual can be found [here](./docs/installation_manual.md "Installation Manual").

## Project Description

The application is a simple and limited movie rating website. User can register and login, add new movies and rate them (their own and others). Rating consists of a star rating from 1-10 and a free-form comment. When adding a movie, user must provide the movie title & category (e.g. comedy, drama, action, etc.).

User can also delete their own ratings. User cannot delete their own movie, **if someone else has rated it**. User can also view other users' ratings and movies. Movies can be searched by title and sorted by the ratings they have received.

Movies are divided into categories.

The application also has superusers (no registration possibility, added during database creation), who can (in addition to all the features of a regular user) delete any movies and ratings. Superusers can also change the name and category of individual movies.

## Admin Users

Pre-populated superusers:

```
alice:redqueen
bob:squarepants
patrick:asteroid
```
