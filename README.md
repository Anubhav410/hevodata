# hevodata

## Setup Virtual Environment
`python -m venv venv`

## Activate Virtual Environment
`source ./venv/bin/activate`

## Install Dependencies
`pip install -r requirements.txt`

## Setup Database

* Install and Setup PSQL
* Make a copy of .devdefaults file in `/env` folder, and name it `.dev`
* Update the Secrets in this file

## Run Migrations
`python manage.py runserver`

