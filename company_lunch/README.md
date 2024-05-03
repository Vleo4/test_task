# LunchDecider - the most necessary service

### INFORCE PYTHON TASK

## Installation

#### Run server and setup project

```
docker-compose up --build
```

#### Run tests

```
pip install -r requirements.txt
pytest
```

### Tests may not work on development environment, change
```
DJANGO_ENVIRONMENT=development
```
#### to 
```
DJANGO_ENVIRONMENT=testing
```
#### in .env file

## API guide

### Some endpoints require "Authorization" header
```
Bearer your_token
```
