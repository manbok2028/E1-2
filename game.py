"""메뉴와 게임 흐름을 관리하는 QuizGame 클래스."""

from __future__ import annotations

from pathlib import Path

from quiz import Quiz
from storage import load_state, save_state


class QuizGame:
    """퀴즈 목록·점수·메뉴 동작을 한곳에서 관리한다."""

    def __init__(self, state_path: Path | None = None) -> None:
        self.state_path = state_path or Path(__file__).resolve().parent / "state.json"
        self.quizzes, self.best_score, self.history, self.load_message = load_state(self.state_path)
        self.running = True

    def save(self) -> None:
        success, message = save_state(self.state_path, self.quizzes, self.best_score, self.history)
        print(f"📁 {message}" if success else f"⚠️ {message}")

    def show_menu(self) -> None:
        print("\n" + "=" * 44)
        print("          🎯 우리 문화 퀴즈 게임 🎯")
        print("=" * 44)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제 (보너스)")
        print("6. 종료")
        print("=" * 44)

    def ask_number(self, prompt: str, minimum: int, maximum: int) -> int:
        """공백·빈 값·문자·범위 밖 수를 모두 다시 입력하게 한다."""
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("⚠️ 아무것도 입력되지 않았습니다. 다시 입력하세요.")
                continue
            try:
                number = int(raw_value)
            except ValueError:
                print(f"⚠️ 숫자로 입력하세요. {minimum}부터 {maximum} 사이입니다.")
                continue
            if not minimum <= number <= maximum:
                print(f"⚠️ {minimum}부터 {maximum} 사이의 숫자를 입력하세요.")
                continue
            return number

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"  [{number}] {quiz.question}")

    def run(self) -> None:
        print(f"\n📂 {self.load_message}")
        try:
            while self.running:
                self.show_menu()
                choice = self.ask_number("선택: ", 1, 6)
                if choice == 3:
                    self.list_quizzes()
                elif choice == 6:
                    self.running = False
                    print("👋 다음에 또 만나요!")
                else:
                    print("🚧 이 기능은 다음 단계에서 완성됩니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되었습니다. 현재 데이터를 저장하고 안전하게 종료합니다.")
        finally:
            self.save()
