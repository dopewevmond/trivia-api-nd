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
createbd trivia
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

## Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

Example request: `curl https://trivia-baseurl/categories`
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```


`GET '/questions'`

- Fetches a paginated list where each element in the list is a dictionary that contains a question. 
- Request Arguments: a query parameter `page` (optional) - the page number to be used for pagination
- Returns: an object with the following keys
  - `questions`: a list of questions
  - `totalQuestions`: the number of questions returned
  - `categories`: a dictionary whose keys are the IDs of the categories and the values are the category names
  - `success`: a boolean value which indicates the success of the request

Example request: `curl https://trivia-baseurl/questions`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "totalQuestions": 2,
  "questions": [
    {
      "answer": "Maya Angelou",
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Apollo 13",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ]
}
```


`DELETE '/questions/<int:question_id>'`

- Deletes a question with an ID of `question_id`
- Request Arguments: `question_id` in path - the ID of the question to delete
- Returns: 
  - A 404 error if a question with ID of `question_id` was not found
  - An object with a key `success` which has a boolean value containing the status of the request

Example request: `curl -X DELETE https://trivia-baseurl/questions/2`
```json
{
  "success": true
}
```

`POST '/questions'`

This endpoint either posts a new question to the database or searches for an existing question in the database. 
- To search for an existing question in the database: &nbsp; &nbsp;
  - Request Arguments: a dictionary with a key `searchTerm` - it's value is a substring to search for a question.
  - Returns: a dictionary containing the following keys
    - `success`: a boolean value containing the status of the request
    - `questions`: a list of questions which `searchTerm` is a substring of
    - `totalQuestions`: the number of questions of which `searchTerm` is a substring of

  Example request: `curl -X POST -d '{"searchTerm": "hanks"}' -H "Content-Type: application/json" https://trivia-baseurl/questions`
    ```json
    {
      "success": true,
      "totalQuestions": 1,
      "questions": [
        {
          "answer": "Apollo 13",
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
      ]
    }
    ```
- To post a new question in the database:
  - Request Arguments: a dictionary with keys
    - `question` - the question to add to the database.
    - `answer` - the answer to the question.
    - `difficulty` - the difficulty of the question on a scale of 1-5 where 5 is the most difficult.
    - `category` - the ID of the category to which the question belongs <br>
  - Returns: a dictionary containing the following keys
    - `success`: a boolean value containing the status of the request

  Example request: `curl -X POST -d '{"question":"Where does the sun rise?","answer":"The east","difficulty":2,"category":1}' -H "Content-Type: application/json" https://trivia-baseurl/questions`
    ```json
    {
      "success": true
    }
    ```

`GET '/categories/<int:category_id>/questions'`
- Fetches a list of questions which all belong to a category with ID `category_id`
- Request Arguments: `category_id` in path - ID of category to get questions for
- Returns: an object with the following keys
  - `currentCategory`: the category to which the questions belong
  - `questions`: a list of questions
  - `totalQuestions`: the number of questions returned
  - `success`: a boolean value which indicates the success of the request

Example request: `curl https://trivia-baseurl/categories/4/questions`
```json
{
  "currentCategory": "History",
  "totalQuestions": 2,
  "success": true,
  "questions": [
    {
      "answer": "Maya Angelou",
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Scarab",
      "difficulty": 4,
      "id": 5,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ]
}
```

`POST '/quizzes'`

- Fetches questions to be used to play the game
- Request Arguments: a dictionary with keys
    - `previous_questions` - a list containing the IDs of every question that the user has already seen or answered
    - `quiz_category` - the ID of the category to fetch questions for. It should be `0` if you want to fetch all questions irrespective of their categories.
- Returns: an object with the following keys
  - `success`: a boolean value which indicates the success of the request
  - `question`: an object which contains a random question that has not yet been answered by the user

Example request: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": 0}' https://trivia-baseurl/quizzes`

```json
{
  "success" : true,
  "question": {
      "answer": "Scarab",
      "difficulty": 4,
      "id": 5,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
