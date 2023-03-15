# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


---

## Endpoints

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return the following error types when requests fail, the column titles corresponding with where it populates the above json example:

| **Error** | **Message**             |
|-----------|-------------------------|
| 400       | `Bad Request`           |
| 404       | `Resource Not Found`    |
| 405       | `Method Not Allowed`    |
| 422       | `Unprocessable Entity`  |
| 500       | `Internal Server Error` |

### Retrieve categories
#### `GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A boolean success and an object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

##### Sample request
```json
curl http://127.0.0.1:5000/categories
```

##### Sample Response

```json
{
  "success": True,
  "categories": {  
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### Retrieve questions
#### `GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer _(optional)_
- Returns: An object with boolean success, 10 paginated questions, total questions, object including all categories, and current category string

##### Sample request
```json
curl http://127.0.0.1:5000/questions?page=2
```

##### Sample Response

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

### Delete a question
#### `DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code and boolean success.

##### Sample request
```json
curl -X DELETE \
  http://127.0.0.1:5000/questions/2
```

##### Sample Response

```json
{
  "success": True
}
```

---

### Create a question
#### `POST '/questions'`

- Sends a post request in order to add a new question
- Returns: Does not return any new data except boolean success

##### Sample request

```json
curl -X POST \
  -h "Content-Type: application/json" \
  -d '{ \
    "question": "Heres a new question string", \
    "answer": "Heres a new answer string", \
    "difficulty": 1, \
    "category": 3 \
  }' \
  'http://localhost:5000/questions/search'
```

##### Sample response

```json
{
  "success": True
}
```

---

### Search questions
#### `POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Returns: a boolean success, any array of questions, a number of totalQuestions that met the search term and the current category string

##### Sample request

```json
curl -X POST \
  -h "Content-Type: application/json" \
  -d '{"searchTerm":"this is the term the user is looking for"}' \
  'http://localhost:5000/questions/search'
```

##### Sample response

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 100,
  "current_category": "Entertainment"
}
```

### Retrieve questions by category
#### `GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: A boolean success, an object with questions for the specified category, total questions, and current category string

##### Sample request

```json
curl 'http://127.0.0.1:5000/categories/2/questions'
```

##### Sample response

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "total_questions": 100,
  "current_category": "History"
}
```

---

### Play quiz
#### `POST '/quizzes'`

- Sends a post request in order to get the next question
- Returns: a boolean success and a single new question object

##### Sample request

```json
curl -X POST \
  -h "Content-Type: application/json" \
  -d '{
    "previous_questions": [1, 4, 20, 15], \
    "quiz_category": { \
        "type": "Science", \
        "id": 1 \
    } \
  }' \
  'http://localhost:5000/quizzes'
```

##### Sample response

```json
{
  "success": True,
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 1
  }
}
```

---

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
