# Coffee Shop Full Stack

## Introduction

Coffee Shop App is a digitally enabled cafe, where students can order drinks, socialize, and study hard. The application API is built around RESTful concepts and it performs all CRUD operations. As part of Udacity Fullstack Nanodegree, it is a project I built using all the concepts and skills I learnt throughout the lesson.

The App does the following with the help of the built API, and the authentication system.

- It display graphics which represent the ratios of ingredients in each drink.
- It allow public users to view drink names and graphics.
- It allow the shop baristas to see the recipe information.
- It allow the shop managers to create new drinks and edit existing drinks.

## Code Style

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Main Files: Project Structure

```
├── README.md
├── .gitignore
├── frontend
│   ├── e2e
│   ├── src
│   ├── package.json
│   ├── package-lock.json
│   ├── angular.json
│   ├── ionic.config.json
│   ├── tsconfig.json
│   ├── tslint.json
└── backend
    ├── src
    │   ├── auth
    |   │   ├── auth.py
    │   ├── database
    |   │   ├── database.db
    |   │   ├── models.py
    │   ├── api.py
    ├── requirements.txt # The dependencies we need to install with `pip3 install -r requirements.txt`
    └── postman collection
```

**Overall**:

- Models are located in `models.py` file
- Controllers are located in `api.py` file
- Authentication is done in `auth.py` file

## Getting Started

### Pre-requisites and Local Development

The prerequites tools for local development are:

- Python
- Pip
- Node
- Ionic CLI
- virtualenv: To create an isolated Python environment

### Backend

It is a good practice to keep your app dependencies isolated by working a virtual environment.

- To Initialize a virtual enviroment, run

```
python -m virtualenv env
```

- To Activate the environment run

```
source env/bin/activate
```

**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```
source env/Scripts/activate
```

To run the backend application, you need to install the required packages by doing the following,

- navigate into the backend folder
- run
  `pip install -r requirements.txt`

After succesfull installation of the packages, you can get the app running by running the following commands

```
export FLASK_APP=api.py
export FLASK_DEBUG=True # enables debug mode
flask run

```

**Note**: For window, change export to set i.e. set FLASK_APP=api.py

The application is launched on `http://127.0.0.1:5000/` by default.

### Frontend

The frontend is designed to work with a Flask-based Backend. You need to get the backend application running first before making a request from the frontend.

The app is built with a JavaScript framework and so there is need to install the frontend dependencies using Node.js and NPM

You can confirm if Node.js and NPM is installed successfully using the codes below

```
node -v
npm -v
```

From the frontend folder, run the following command to install the dependencies

```
npm install # run this once to install project dependencies
```

To get the application running in the local browser, execute the following commands to install the Ionic CLI and get it running.

```
npm install -g @ionic/cli
ionic serve # This will get the frontend app running
```

The application is launched on `http://127.0.0.1:8100/` by default.

### Tests

In order to test the API endpoints, import the postman collection to postman and make a request to each endpoint and then check the test tab.

The postman collection `udacity-fsn0d-udaspicelatte.postman_collection.json` is located in the backend folder.

## API Reference

### Getting Started

This application is not deployed and can only be run locally. The backend application is hosted at the default port (Base URL) which is set as a proxy in the frontend application.

- **Base URL**: http://127.0.0.1:5000/


### Authentication and Authorization

#### Authentication
This application make use of Auth0 authentication system to secure all the endpoints except for sending a 'GET' request to the `/drinks` endpoint. 

`./src/app/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, managing the JWT token upon successful callback, and handle setting and retrieving the token from the local store. 

This token is then consumed by our DrinkService (`./src/app/services/drinks.service.ts`) and passed as an Authorization header when making requests to the backend.

#### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. 

This method is defined in  `./src/app/services/auth.service.ts` and is then used to enable and disable buttons in `./src/app/pages/drink-menu/drink-form/drink-form.html`.

### Error Handling

- **Errors format**: All errors including Authentication errors are returned as a JSON object as shown below

```
{
    'success': False,
    'error': 404,
    'message': "Resources not found"
}
```

- **Error Codes and Messages**: The API will return one out of four(4) error type whenever the request fail:

  - 400: Bad request
  - 404: Resources not found
  - 405: Methods not allowed
  - 422: Request unprocessable

- **Error Mesaages possible solution**:
  - Bad Request: Check the format of your request. Make sure your format satisfies what the endpoint and the endpoint method requires.
  - Resources not found: Search for resources that exist in the database or server
  - Methods not allowed: Check if the method is allowed for the particular endpoint
  - Request unprocessable: Try again! Server error.

- **Authentication Error Codes and Messages**:
    - 400: Invalid Claims
    - 401: Authorization header is not valid
    - 403: Unauthorized

### Endpoints

#### Method: GET

#### Endpoint: /drinks

- General:
  - This endpoint is a public endpoint as no permission is needed to access it.
  - Fetched results is an object with `success` and `drinks` keys.
  - The value of `drinks` is a list and each element of the list is an object that has `id`, `title` and `recipe` keys.
  - Request argument: None

- Sample: `curl http://127.0.0.1:5000/drinks`

- Response: Json

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "sucess": true
}
```

#### Method: GET

#### Endpoint: /drinks-detail

- General:
  - It can only be accessed by users with the `get:drinks-detail` permission.
  - Fetched results is an object with `success` and `drinks` keys.
  - The value of `drinks` is a list and each element of the list is an object that has `id`, `title` and `recipe` keys.
  - Request argument: None

- Sample: `curl http://127.0.0.1:5000/drinks-detail`

- Response: Json

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "sucess": true
}

```

#### Method: POST

#### Endpoint: /drinks

- General:

  - This endpoint use the request body to create a new drink.
  - It can only be accessed by user with the `post:drinks` permission.
  
- Sample: `curl -X POST http://127.0.0.1:5000/drinks -H "Content-Type: application/json" -H "Authorization: Bearer JWT" -d '{"title": "Water3","recipe": [{"name": "Water","color": "blue","parts": 1}]}'`

- Request Body: json

```
  {
    "title": "Water3",
    "recipe": [{
        "name": "Water",
        "color": "blue",
        "parts": 1
    }]
}

```

- Response Body: json

```
{
    "drinks": [
        {
            "id": 2,
            "recipe": {
                "color": "blue",
                "name": "Water",
                "parts": 1
            },
            "title": "Water3"
        }
    ],
    "sucess": true
}
```

#### Method: DELETE

#### Endpoint: /drinks/{delete_id}

- General:
  - This endpoint takes in a drink id of the row to be deleted
  - It can only be accessed by user with the `delete:drinks` permission.
  - Request argument: None

- Sample: `curl http://127.0.0.1:5000/drinks/1`

- Response Body: json

```
{
        'sucess': True,
        'id': delete_id,
}
```

#### Method: PATCH

#### Endpoint: /drinks/{update_id}

- General:
  - This endpoint takes in a drink id of the row to be updated together with a body cointaining new detail.
  - It can only be accessed by user with the `patch:drinks` permission.
  - No request argument needed.

- Sample: `curl -X POST http://127.0.0.1:5000/drinks/1 -H "Content-Type: application/json" -H "Authorization: Bearer JWT" -d '{"title": "Water","recipe": [{"name": "Water","color": "blue","parts": 1}]}'`

- Request Body: json

```
  {
    "title": "Water5",
    "recipe": [{
        "name": "Water",
        "color": "blue",
        "parts": 1
    }]
}

```

- Response Body: json

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "sucess": true
}
```



## Author

Elijah Lawal Ismaila

