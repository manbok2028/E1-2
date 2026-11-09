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
        if not self.question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(self.choices) != 4 or any(not item.strip() for item in self.choices):
            raise ValueError("선택지는 비어 있지 않은 4개여야 합니다.")
        if self.answer not in range(1, 5):
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
        return cls(
            question=str(payload["question"]),
            choices=[str(choice) for choice in payload["choices"]],  # type: ignore[index]
            answer=int(payload["answer"]),
            hint=str(payload.get("hint", "")),
        )
