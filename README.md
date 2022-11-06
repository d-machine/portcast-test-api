# portcast-test-api

## Description:

Thsi repository includes api with endpoints `/api/get`, `/api/search` and `/api/dictionary` using django framework.
FileStorage is used for storing paragraphs and postgres is used for storing the count of words for dictionary api. Both pgdata and filestorage locations are mapped to a location outside the docker container so that the data can be persisted even after removing the docker images. Code for all the apis reside inside app/portcast/api directory.

Before using the code please make sure docker is running

## Building the image

```
docker-compose build
```

## Running the server

```
docker-compose up
```

### For running the testcases run the following command

```
docker-compose run --rm app sh -c "python manage.py test"
```

## For testing the api

### For Get api open following url in browser tab or postman

> http://localhost:8000/api/get

### For Search api open following url in browser tab or postman

Please Note: This endpoint requires two query_params -

- keywords: comma separated list of words
- operator: "or" or "and"

> http://localhost:8000/api/search?keywords=the,moment&operator=and

### For dictionary api open following url in browser tab or postman

> http://localhost:8000/api/dictionary
