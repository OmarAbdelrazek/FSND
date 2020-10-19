# Trivia API

## Installing Dependencies
* Python 3.7:
install the latest version of python for your platform from [here](https://www.python.org/downloads/)

* Virtual Enviornment:
Python virtual environments is to create an isolated environment for Python projects. This means that each project can have its own dependencies, regardless of what dependencies every other project has, Instructions for setting up a virual enviornment [here](https://docs.python.org/3/tutorial/venv.html)

* Project Dependencies:
install requirements by:
  - Go to ```/backend``` directory.
  - ```bash
    pip install -r requirements.txt
    ```
* Run Server:
  - Execute the following: 
  ```bash
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run
  ```

## Getting Started

- Base URL: The Backend App is hosted localy ```127.0.0.1:5000 ```.
- Authintication: Currently its not require authintication or API Keys.

## Error Handling
Error's are returned as JSON objects in the following format:
```
{
  "success": False,
  "message": "resource not found",
  "code": 404
}
```
The API has 4 types of errors:
1) 400: Bad Request.
2) 404: Resource Not Found.
3) 405: Method Not Allowed.
4) 422: Unprocessable.

## Endpoints
# GET /categories
* General:
  - Returns a list of categories objects and success value.
* Sample: ``` curl http://127.0.0.1:5000/categories ```
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
# GET /questions
* General:
  - Returns a list of questions objects, list of categries objects, success value and number of total questions
  - Result are paginated in groups of 10 questions per page, and pages are starting from 1.
* Sample: ``` curl http://127.0.0.1:5000/questions?page=1 ```
  ```sh
  {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": "4",
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": "4",
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": "3",
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": "3",
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": "3",
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 38
    } 
    ```



# POST /questions
* General:
  - Creates a new question usuing submitted question, answer, category and difficulty.
* Sample:  ``` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d
             '{
                'question': 'q1',
                'answer': 'a1',
                'category': 2,
                'difficulty': 3
              }'   
            ```
 ```sh
 {
    "categories": {
        "1": "Science"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": "4",
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": "4",
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": "3",
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": "3",
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": "3",
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 39
}
```
                          
              
# DELETE /questions/{question_id}
* General: Delete the question of the given id if its exists, Return success value, questions, number of total questions and categories. 
* Sample: ``` curl -X DELETE http://127.0.0.1:5000/questions/1 ```
```
{
    "categories": {
        "1": "Science"
    },
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": "4",
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": "3",
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": "3",
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": "3",
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
    "total_questions": 38
}
```
# POST /questions/search
* General: Search question by any phrase by given search term, Returns success value, questions and number of total questions
* Sample: ``` curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d
             '{
                'searchTerm': 'who'
              }'   
            ```
            
```
{
    "questions": [
        {
            "answer": "George Washington Carver",
            "category": "4",
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": "1",
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```


# GET /categories/{category_id}/questions
* General: Get question by given category_id, Retuens success value, questions, number of total questions and current category.
* Sample: ``` curl -X GET http://127.0.0.1:5000/categories/1/questions ```
```
{
    "current_category": "Science",
    "questions": [
        {
            "answer": "The Liver",
            "category": "1",
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": "1",
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": "1",
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```
# POST /play 
* General: Get questions to play the quiz this takes the category and previous question as an array and returns random question and success value.
* Sample: ```  curl http://127.0.0.1:5000/play -X POST -H "Content-Type: application/json" -d
             '{
                'category': 1,
                'previous_questions': []
              }'   
            ```
```
{
    "question": {
        "answer": "Alexander Fleming",
        "category": "1",
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```
            
# Test Cases:
To run the test cases execute the following:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

