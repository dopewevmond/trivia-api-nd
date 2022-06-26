import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        return jsonify({
            "success": True,
            "categories": categories_dict
        }), 200


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        categories = [category.format() for category in categories]
        categories_dict = {}
        for category in categories:
            categories_dict[category['id']] = category['type']
        
        current_questions = [question.format() for question in questions[start:end]]
        if not current_questions:
            abort(404)
        
        return jsonify({
            "questions": current_questions,
            "totalQuestions": len(questions),
            "success": True,
            "categories": categories_dict,
            "currentCategory": categories[0]
        }), 200

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404)
        success = True
        try:
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
            success = False
        finally:
            db.session.close()
        if not success:
            abort(500)
        return jsonify({
            'success': True
        }), 200
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        req_body = request.get_json()
        search_term = req_body.get('searchTerm')
        if search_term:
            search_results = Question.search(search_term)
#             if search_results.count() == 0:
#                 abort(404)
            search_results = search_results.all()
            questions = [question.format() for question in search_results]
            totalQuestions = len(questions)
            return jsonify({
                'success': True,
                'questions': questions,
                'totalQuestions': totalQuestions
            }), 200
        
        else:
            text = req_body.get('question')
            answer = req_body.get('answer')
            difficulty = req_body.get('difficulty')
            category = req_body.get('category')
            
            bad_request = len(list(filter(lambda x: x is None, [text, answer, difficulty, category]))) > 0
            if bad_request:
                abort(400)
                
            success = True
            try:
                question = Question(question=text, answer=answer, category=category, difficulty=difficulty)
                db.session.add(question)
                db.session.commit()
            except:
                db.session.rollback()
                success = False
            finally:
                db.session.close()
            if success:
                return jsonify({
                    'success': success
                })
            
            abort(422)
        

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        category_id = category.id
        questions = Question.query\
                    .filter_by(category=category_id)\
                    .all()
        questions = [question.format() for question in questions]
        currentCategory = category.type
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': currentCategory
        }), 200
        

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        req_body = request.get_json()
        
        previous_questions = req_body.get('previous_questions')
        quiz_category = req_body.get('quiz_category')
        
        if previous_questions is None or not quiz_category:
            abort(400)
        
        questions = Question.query
        if quiz_category['id'] == 0:
            questions = questions.all()
        else:
            questions = questions.filter_by(category=quiz_category['id']).all()
        
        num_questions = len(questions)
        if num_questions == 0:
            abort(404)
        if num_questions == len(previous_questions):
            return jsonify({
                'success': True
            }), 200
        
        random_number = random.randrange(num_questions)
#         print(f'This is our first random number {random_number}')
#         print('this is the list containing our previous questions', previous_questions)
        while (random_number in previous_questions):
            random_number = random.randrange(num_questions)
#             print(f'this {random_number} was generated in the while loop')
#             print('these are the previous questions', previous_questions)
        # now we can be sure that this question has not been shown to the user
        chosen_question = questions[random_number]
        return jsonify({
            'success': True,
            'question': chosen_question.format()
        }), 200
            
        

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Not allowed"
        }), 405
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable request"
        }), 422
    
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
