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
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories_post_not_allowed(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        
    def test_categories_put_not_allowed(self):
        res = self.client().put('/categories')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
    
    def test_categories_patch_not_allowed(self):
        res = self.client().patch('/categories')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
    
    def test_categories_delete_not_allowed(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
    
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        
    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['success'])
        self.assertTrue(data['currentCategory'])
        
    def test_get_questions_failure_exceed_limit(self):
        res = self.client().get('/questions?page=2000')
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
#     def test_delete_question_success(self):
#         res = self.client().delete('/questions/2')
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(data['success'])        
        
    def test_delete_question_failure_does_not_exist(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_get_on_delete_question_endpoint_failure(self):
        res = self.client().get('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        
    def test_post_new_question_success(self):
        res = self.client().post('/questions', json={'question': 'Where does the sun rise?', 'answer': 'The East', 'difficulty': 2, 'category': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_post_new_question_failure(self):
        """omitting some values from the request body"""
        res = self.client().post('/questions', json={'difficulty': 5, 'answer': 'The East', 'category': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        
    def test_search_questions_success(self):
        res = self.client().post('/questions', json={'searchTerm': 'largest'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
    
    def test_questions_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        
    def test_questions_by_category_failure(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_quizzes_endpoint_success(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': 2})
        data = json.loads(res)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()