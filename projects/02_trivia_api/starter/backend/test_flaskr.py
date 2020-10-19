import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:12345@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'q1',
            'answer': 'a1',
            'category': 2,
            'difficulty': 3
        }

        self.new_question_missing_fields = {
            'question': 'q1m',
            'category': 3,
            'difficulty': 1
        }

        self.play = {
            'previous_questions': [6, 11, 19, 21],
            'category': 0
        }

        self.play_with_invalid_category = {
            'previous_questions': 1000,
            'category': 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])




    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((data['total_questions']))
        self.assertTrue((data['questions']))
        self.assertTrue((data['categories']))

    def test_404_get_all_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue((data['total_questions']))
        self.assertTrue((data['questions']))
        self.assertTrue((data['categories']))

    def test_400_new_question(self):
        res = self.client().post('/questions', json=self.new_question_missing_fields)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')



    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter_by(id = 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue((data['total_questions']))
        self.assertTrue((data['categories']))
        self.assertEqual(question,None)
        self.assertEqual(data['success'], True)

    def test_question_doesnt_exist_404(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(data['success'], False)



    def test_question_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'How'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((data['total_questions']))
        self.assertTrue((data['questions']))

    def test_404_question_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'Omar'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_question_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')


    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((data['total_questions']))
        self.assertTrue((data['questions']))
        self.assertTrue((data['current_category']))

    def test_404_get_question_by_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_play(self):
        res = self.client().post('/play', json=self.play)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((data['question']))

    def test_422_play(self):
        res = self.client().post('/play', json=self.play_with_invalid_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()