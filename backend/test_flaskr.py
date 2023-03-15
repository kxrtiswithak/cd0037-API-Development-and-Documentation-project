import os
import unittest
import json
import subprocess
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv, find_dotenv

# env_file = find_dotenv((".env.shared"))
load_dotenv(".env.shared")

TEST_DB_HOST = os.environ.get('DB_HOST', 'localhost:5432')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME', 'trivia_test')
TEST_DB_USER = os.environ.get('DB_USER', 'student')
TEST_DB_PASSWORD = os.environ.get('DB_PASSWORD', 'student')
TEST_DB_PATH = 'postgresql://{}:{}@{}/{}'.format(
    TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_HOST, TEST_DB_NAME
)


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = TEST_DB_PATH
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "fooQuestion",
            "answer": "fooAnswer",
            "difficulty": 1,
            "category": 1
        }

        self.search = {
            "searchTerm": "the"
        }

        self.quiz_body = {
            "previous_questions": [],
            "quiz_category": {
                "type": "Science",
                "id": 1
            }
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_retrieve_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_405_for_post_categories(self):
        res = self.client().post("categories")

        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 405)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "method not allowed")

    def test_retrieve_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], 0)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_404_retrieve_question_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 404)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])

    def test_404_delete_question_that_doesnt_exist(self):
        res = self.client().delete("/questions/7000")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 404)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_create_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])

    def test_405_for_create_question(self):
        res = self.client().post("/questions/7", json=self.new_question)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 405)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "method not allowed")

    def test_search_questions(self):
        res = self.client().post("/questions/search", json=self.search)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], 0)

    def test_405_for_search_questions_with_wrong_method(self):
        res = self.client().get("/questions/search", json=self.search)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 405)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "method not allowed")

    def test_404_for_search_questions_with_wrong_path(self):
        res = self.client().post("/questions/search/7", json=self.search)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 404)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_404_for_search_questions(self):
        res = self.client().post(
            "/questions/search",
            json={"searchTerm": "qwertyuiop"}
        )
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 404)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_retrieve_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], 1)

    def test_404_retrieve_questions_by_category(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 404)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        res = self.client().post("/quizzes", json=self.quiz_body)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 200)  # type: ignore
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_405_play_quiz(self):
        res = self.client().get("/quizzes", json=self.quiz_body)
        data = json.loads(res.data)  # type: ignore

        self.assertEqual(res.status_code, 405)  # type: ignore
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "method not allowed")


if __name__ == "__main__":
    unittest.main()
