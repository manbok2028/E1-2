"""퀴즈 한 문제를 표현하는 도메인 클래스."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Quiz:
    """문제, 네 개의 선택지, 정답 번호를 한 묶음으로 관리한다."""

    question: str
    choices: list[str]
    answer: int
    hint: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if (
            not isinstance(self.choices, list)
            or len(self.choices) != 4
            or any(not isinstance(item, str) or not item.strip() for item in self.choices)
        ):
            raise ValueError("선택지는 비어 있지 않은 4개여야 합니다.")
        if isinstance(self.answer, bool) or not isinstance(self.answer, int) or self.answer not in range(1, 5):
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")

    def display(self) -> str:
        """콘솔에 보여 줄 문제와 선택지 문자열을 만든다."""
        lines = [self.question]
        lines.extend(f"  {number}. {choice}" for number, choice in enumerate(self.choices, start=1))
        return "\n".join(lines)

    def is_correct(self, selected_number: int) -> bool:
        """사용자가 고른 번호가 정답인지 알려 준다."""
        return selected_number == self.answer

    def to_dict(self) -> dict[str, object]:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Quiz":
        if not isinstance(payload, dict):
            raise ValueError("퀴즈 데이터는 객체 형태여야 합니다.")
        question = payload.get("question")
        choices = payload.get("choices")
        answer = payload.get("answer")
        hint = payload.get("hint", "")
        if not isinstance(question, str) or not isinstance(choices, list):
            raise ValueError("퀴즈의 문제와 선택지 형식이 올바르지 않습니다.")
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise ValueError("퀴즈의 정답 번호 형식이 올바르지 않습니다.")
        if not isinstance(hint, str):
            raise ValueError("퀴즈의 힌트 형식이 올바르지 않습니다.")
        return cls(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
