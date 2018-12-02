# Celery-Flask-MongoDB REST App
RESTful app for fetching, storing and serving text and image data from websites

Flask/connexion app defined in OpenAPI standard passing requests to celery worker.
Celery is connected with Redis broker and backend to persist task statuses. Images are stored in the filesystem.
An instance of MongoDB stores their filenames and text data. Deployed with Docker.

## Run:

`cp .env.example .env` - configure necessary environment variables
<br>`docker-compose up` - run containers

At default service UI can be accessed at `localhost:8000/ui/`

## Test locally:

`python3 -m virtualenv venv`
<br>`source venv/bin/activate`
<br>`pip install -r requirements.txt`
<br>`pytest`

## Design

- /ml/content/images/{url}
    - POST: Save all images from given url
    - GET: Download saved images
- /ml/content/text/{url}
    - POST: Save page text from given url
    - GET: Download saved text
- /ml/content
    - GET: Download all content
- ml/content/[images, text]/{task_id}
    - GET: check status for given task_id in headers.locations
<br><br><b>Note:</b> the app is currently defined with swagger 2.0 specification. Swagger-ui has been found to supply corrupted links for Content-Disposition file responses. Until the definition is not updated to OpenApi 3.0 please use direct endpoint urls (such as 'localhost:8000/ml/content') when testing with swagger-ui.

## TODOS

- Modify currently ad hoc MongoDB client instantiation for each task
- Set MongoDB instance as Celery backend (at the moment celery lacks support for mongo)
- Clean the storage periodically/on request
- Update swagger.yaml definition from 2.0 to OpenApi v. 3.0
