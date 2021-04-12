# NotSoSoft

## Setup environment
```
python3.8 -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt
pre-commit install
```

## Management
`Docker` and `docker-compose` need to be present.
```
docker-compose build
docker-compose up
```
### Running migrations
```
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
```
### Running tests
```
pytest
```
