import os
from flask import Flask, request, abort, jsonify, render_template
from flask.globals import current_app
from flask.json import loads
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get('page',1,type= int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_question = questions[start:end]
  return current_question

def create_app(test_config=None):
  # create and configure the app
  
  app = Flask(__name__)
  setup_db(app)
  

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources = {r'/api/*': {"origins" : '*'} })
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, DELETE, PATCH, OPTIONS')

    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''


  @app.route('/categories', methods = ['GET'])
  def get_all_categories():
    categoies = Category.query.all()
    categories= {}
    for category in categoies:
      categories[category.id] = category.type

    return jsonify({
      'categories': categories,
    })

  



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods = ['GET'])
  def get_all_questions():
    questions = Question.query.all()
    all_categoies = Category.query.all()
    current_questions = paginate_questions(request,questions)
    categories = {}

    for category in all_categoies:
      categories[category.id] = category.type


    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'questions': current_questions,

      'total_questions': len(questions),

      'categories': categories
    })
      


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<int:question_id>",methods= ['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter_by(id = question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()

      questions = Question.query.all()
      all_categoies = Category.query.all()
      current_questions = paginate_questions(request,questions)
      categories = {}

      for category in all_categoies:
        categories[category.id] = category.type
        return jsonify({
        'questions': current_questions,

        'total_questions': len(questions),

        'categories': categories
      })
    except:
      abort(422)

    
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_new_question():
    body = request.get_json()
    question = body.get('question',None)
    answer = body.get('answer',None)
    category = body.get('category',None)
    difficulty = body.get('difficulty', 0)
    try:
      new_question = Question(question,answer,category,difficulty)
      new_question.insert()
      questions = Question.query.all()
      all_categoies = Category.query.all()
      current_questions = paginate_questions(request,questions)
      categories = {}

      for category in all_categoies:
        categories[category.id] = category.type
        return jsonify({
        'questions': current_questions,

        'total_questions': len(questions),

        'categories': categories
      })
    except:
      abort(422)



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search():
    body = request.get_json()
    search_question = body.get('searchTerm','')
    result = Question.query.filter(Question.question.ilike("%"+search_question+"%")).all()
    questions = [question.format() for question in result]
    
    return jsonify({
      'questions': questions,
      'total_questions': len(questions)
    })
    

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_questions_by_category(category_id):
    category = Category.query.filter_by(id = category_id).one_or_none()
    if category is None:
      abort(404)
    result = Question.query.filter(Question.category.ilike(category.type)).all()
    if len(result) == 0:
      abort(404)
    questions = paginate_questions(request,result)
    return jsonify({
      'questions' : questions,
      'total_questions': len(questions),
      'current_category': category.type
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

    