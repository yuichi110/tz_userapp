# python-web-app
## Python Flask Web App 
### How to run locally

0. install poetry
1. cd to project root
2. poetry update
3. poetry run gunicorn  -w 1 -b 0.0.0.0:8000 --reload userapp.__main__:app

### How to test
#### unit test
poetry run pytest

#### external api test
poetry python tests/external/test_api.py
you can configure PROTOCOL(http/https), HOST, PORT via env

### API DOC

#### get users (debug)
method: GET
URI: /api/users
REQUEST BODY:
RESPONSE BODY: [{id:<user-uuid>, username:<user-name>, email:<email>},...]

#### get user
method: GET
URI: /api/users/<signin-username>
REQUEST BODY:
RESPONSE BODY: {id:<user-uuid>, username:<user-name>, email:<email>}
requires signin first. requesting other username returns error

#### signin
method: POST
URI: /api/signin
REQUEST BODY: {username_or_email:<username-or-email>, password:<password>}
RESPONSE BODY: {}

#### signout
method: DELETE
URI: /api/signin
REQUEST BODY:
RESPONSE BODY: {}

#### signup
method: POST
URI: /api/users
REQUEST BODY: {username:<username>, email:<email>, password1:<password>, password2:<password>}
RESPONSE BODY: {}

### Architecture

`__main__.py`: 
Entry point. flask app controller. Serialize/Deserialize JSON and Data Object. Handles error.
Other modules don't depend on flask.
So, you can switch to another framework easily such as FastAPI.

`parameter.py`: load parameters from environment variable and CLI option
`di.py`: inject dependencies(repositories) to service by parameters.
`models/`: Data model.

`services/`: bussiness logic
`repositories/`:
Data layer.
Called by service with "Dependency Inversion" rule.
Currently, using mock repositories for user and session.
However able to add another repositories such as DB/Cache without chainging buiseness logic of service etc.

tests/ holds unittest codes.

## Tanzu Application Platform

