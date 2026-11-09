"""UTF-8 JSON 상태 파일을 안전하게 읽고 쓰는 기능."""

from __future__ import annotations

import json
from pathlib import Path

from default_data import create_default_quizzes
from quiz import Quiz


def default_state() -> tuple[list[Quiz], int, list[dict[str, object]]]:
    return create_default_quizzes(), 0, []


def load_state(path: Path) -> tuple[list[Quiz], int, list[dict[str, object]], str]:
    """상태를 불러오고, 문제가 있으면 기본 상태와 안내 문구를 반환한다."""
    if not path.exists():
        quizzes, best_score, history = default_state()
        return quizzes, best_score, history, "저장 파일이 없어 기본 퀴즈로 시작합니다."

    try:
        with path.open("r", encoding="utf-8") as state_file:
            payload = json.load(state_file)
        quizzes = [Quiz.from_dict(item) for item in payload["quizzes"]]
        best_score = int(payload.get("best_score", 0))
        history = list(payload.get("history", []))
        return quizzes, best_score, history, f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)"
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        quizzes, best_score, history = default_state()
        return quizzes, best_score, history, f"저장 파일을 읽지 못해 기본 퀴즈로 복구했습니다. ({error.__class__.__name__})"


def save_state(path: Path, quizzes: list[Quiz], best_score: int, history: list[dict[str, object]]) -> tuple[bool, str]:
    """상태를 UTF-8 JSON으로 저장하고 성공 여부를 반환한다."""
    payload = {
        "quizzes": [quiz.to_dict() for quiz in quizzes],
        "best_score": best_score,
        "history": history,
    }
    try:
        with path.open("w", encoding="utf-8") as state_file:
            json.dump(payload, state_file, ensure_ascii=False, indent=2)
        return True, "저장했습니다."
    except OSError as error:
        return False, f"저장하지 못했습니다. ({error.__class__.__name__})"
