import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def get_categories():
    categories = Category.query.all()
    categories_dict = {}

    for category in categories:
        categories_dict[category.id] = category.type

    return categories_dict


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Credentials", "*")

        return response

    @app.route("/categories")
    def retrieve_categories():

        return jsonify({
            "success": True,
            "categories": get_categories()
        })

    @app.route("/questions")
    def retrieve_questions(category=0):
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": category,
            "categories": get_categories()
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True
                # "id": question_id
            })

        except SQLAlchemyError as e:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()  # type: ignore

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category
            )

            question.insert()

            return jsonify({
                "success": True
            })

        except SQLAlchemyError as e:
            abort(422)

    @app.route("/questions/search", methods=["POST"])
    def search_questions(category=0):
        search_term = request.json.get("searchTerm")  # type: ignore

        try:
            selection = Question.query.order_by(
                Question.id
            ).filter(
                Question.question.ilike(
                    f"%{search_term}%"
                )
            ).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": category
            })

        except SQLAlchemyError as e:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == category_id).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": category_id
            })

        except SQLAlchemyError as e:
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()  # type: ignore

        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        if quiz_category:
            category_id = quiz_category["id"]

            if category_id == 0:
                selection = Question.query.all()
            else:
                selection = Question.query.filter(
                    Question.category == category_id
                ).all()

            total_questions = len(selection)
            if total_questions == len(previous_questions):
                return jsonify({
                    "success": True
                })

            random_question = random.choice(selection)

            while random_question.format()["id"] in previous_questions:
                selection.remove(random_question)
                random_question = random.choice(selection)

            return jsonify({
                "success": True,
                "question": random_question.format()
            })
        else:
            abort(404)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }),
            405,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable entity"
            }),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }),
            500,
        )

    return app
