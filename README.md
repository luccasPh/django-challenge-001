## Prerequisites

- [Python 3](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Git](https://git-scm.com/)


In order to Run this API in development mode, one should:

- For Linux users need to install this packages
    `sudo apt install python3-dev libpq-dev`
    
- Install project dependencies:
    `poetry install`

- Activate the environment:
    `poetry shell`

- Run docker compose :
    `docker-compose up`

- Run migrate:
    `python app/manage.py migrate`

- Create a superuser by running 
    `python app/manage.py createsuperuser`

- You can test the dev API with the swagger.
    http://localhost:8000/api/docs
    - To run tests.
      `python app/manage.py test app`

*************************************************************************************************************************

In order to Run this API in production mode, do it instead:

- Stop containers:
    `docker-compose stop`
    
- Run docker-compose prod:
    `docker-compose -f docker-compose.prod.yml up -d`

- Create a superuser by running 
    `docker-compose run app bash -c "python manage.py createsuperuser"`
    - To know your container_id, run docker ps and find the django-challenge-001_app id.
    
- You can test the prod API with the postman collection located on this repository.
    http://localhost:8000/api


**************************************************************************************************************************

# Jungle Devs - Django Challenge #001

## Description

**Challenge goal**: The purpose of this challenge is to give an overall understanding of a backend application. You’ll be implementing a simplified version of a news provider API. The concepts that you’re going to apply are:

- REST architecture;
- Authentication and permissions;
- Data modeling and migrations;
- PostgreSQL database;
- Query optimization;
- Serialization;
- Production builds (using Docker).

**Target level**: This is an all around challenge that cover both juniors and experience devs based on the depth of how the concepts were applied.

**Final accomplishment**: By the end of this challenge you’ll have a production ready API.

## Acceptance criteria

- Clear instructions on how to run the application in development mode
- Clear instructions on how to run the application in a Docker container for production
- A good API documentation or collection
- Login API: `/api/login/`
- Sign-up API: `/api/sign-up/`
- Administrator restricted APIs:
  - CRUD `/api/admin/authors/`
  - CRUD `/api/admin/articles/`
- List article endpoint `/api/articles/?category=:slug` with the following response:
```json
[
  {
    "id": "39df53da-542a-3518-9c19-3568e21644fe",
    "author": {
      "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
      "name": "Author Name",
      "picture": "https://picture.url"
    },
    "category": "Category",
    "title": "Article title",
    "summary": "This is a summary of the article"
  },
  ...
]
```
- Article detail endpoint `/api/articles/:id/` with different responses for anonymous and logged users:

    **Anonymous**
    ```json
    {
      "id": "39df53da-542a-3518-9c19-3568e21644fe",
      "author": {
        "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
        "name": "Author Name",
        "picture": "https://picture.url"
      },
      "category": "Category",
      "title": "Article title",
      "summary": "This is a summary of the article",
      "firstParagraph": "<p>This is the first paragraph of this article</p>"
    }
    ```

    **Logged user**
    ```json
    {
      "id": "39df53da-542a-3518-9c19-3568e21644fe",
      "author": {
        "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
        "name": "Author Name",
        "picture": "https://picture.url"
      },
      "category": "Category",
      "title": "Article title",
      "summary": "This is a summary of the article",
      "firstParagraph": "<p>This is the first paragraph of this article</p>",
      "body": "<div><p>Second paragraph</p><p>Third paragraph</p></div>"
    }
    ```
