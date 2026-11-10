"""표준 라이브러리 unittest만 사용한 핵심 동작 테스트."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from default_data import create_default_quizzes
from game import QuizGame
from quiz import Quiz
from storage import load_state, save_state


class QuizAndStorageTests(unittest.TestCase):
    def test_quiz_checks_answer_and_serializes(self) -> None:
        quiz = Quiz("테스트 문제", ["가", "나", "다", "라"], 2, "두 번째")
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()).answer, 2)

    def test_default_quizzes_are_six_or_more(self) -> None:
        self.assertGreaterEqual(len(create_default_quizzes()), 5)

    def test_default_tax_quizzes_reflect_quiz_game_topics(self) -> None:
        questions = [quiz.question for quiz in create_default_quizzes()]
        self.assertTrue(any("국세가 아닌" in question for question in questions))
        self.assertTrue(any("종합소득세" in question for question in questions))
        self.assertTrue(any("원천징수" in quiz.choices for quiz in create_default_quizzes()))
        self.assertTrue(any("부가가치세" in question for question in questions))
        self.assertTrue(any("경정청구" in quiz.choices for quiz in create_default_quizzes()))

    def test_missing_and_corrupt_state_recover_to_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            quizzes, _, _, message = load_state(path)
            self.assertGreaterEqual(len(quizzes), 5)
            self.assertIn("기본", message)
            path.write_text("{broken", encoding="utf-8")
            quizzes, _, _, message = load_state(path)
            self.assertGreaterEqual(len(quizzes), 5)
            self.assertIn("복구", message)

    def test_state_is_saved_as_utf8_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            quizzes = create_default_quizzes()
            success, _ = save_state(path, quizzes, 80, [{"score": 80}])
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(success)
            self.assertEqual(payload["best_score"], 80)
            self.assertEqual(payload["quizzes"][0]["question"], quizzes[0].question)


class GameInputTests(unittest.TestCase):
    def test_number_input_retries_for_empty_text_and_out_of_range(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            game = QuizGame(Path(temporary_directory) / "state.json")
            with patch("builtins.input", side_effect=[" ", "abc", "9", "2"]):
                with redirect_stdout(io.StringIO()):
                    result = game.ask_number("선택: ", 1, 6)
            self.assertEqual(result, 2)

    def test_play_updates_score_and_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            game = QuizGame(Path(temporary_directory) / "state.json")
            first_quiz = game.quizzes[0]
            with patch("game.random.sample", return_value=[first_quiz]):
                with patch("builtins.input", side_effect=["1", str(first_quiz.answer)]):
                    with redirect_stdout(io.StringIO()):
                        game.play_quizzes()
            self.assertEqual(game.best_score, 100)
            self.assertEqual(game.history[-1]["correct_count"], 1)

    def test_eof_exits_safely_and_saves_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            game = QuizGame(path)
            with patch("builtins.input", side_effect=EOFError):
                with redirect_stdout(io.StringIO()) as output:
                    game.run()
            self.assertTrue(path.exists())
            self.assertIn("안전하게 종료", output.getvalue())


if __name__ == "__main__":
    unittest.main()
