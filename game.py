"""메뉴와 게임 흐름을 관리하는 QuizGame 클래스."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import random

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

    def ask_answer(self, quiz: Quiz) -> tuple[int, bool]:
        """정답 번호를 받고, 힌트 사용 여부도 함께 돌려준다."""
        hint_used = False
        while True:
            raw_value = input("정답 번호 (1-4, 힌트는 h): ").strip().lower()
            if raw_value == "h":
                hint_used = True
                print(f"💡 힌트: {quiz.hint or '등록된 힌트가 없습니다.'}")
                continue
            if not raw_value:
                print("⚠️ 아무것도 입력되지 않았습니다. 다시 입력하세요.")
                continue
            try:
                answer = int(raw_value)
            except ValueError:
                print("⚠️ 1부터 4 사이의 숫자 또는 h를 입력하세요.")
                continue
            if answer not in range(1, 5):
                print("⚠️ 정답 번호는 1부터 4 사이여야 합니다.")
                continue
            return answer, hint_used

    def play_quizzes(self) -> None:
        """무작위 문제를 출제하고 점수와 기록을 저장한다."""
        if not self.quizzes:
            print("📭 출제할 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = self.ask_number(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        selected_quizzes = random.sample(self.quizzes, total)
        correct_count = 0
        hint_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제, 순서는 매번 섞입니다.)")
        for number, quiz in enumerate(selected_quizzes, start=1):
            print("\n" + "-" * 44)
            print(f"[문제 {number}] {quiz.display()}")
            answer, hint_used = self.ask_answer(quiz)
            hint_count += int(hint_used)
            if quiz.is_correct(answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 아쉽습니다. 정답은 {quiz.answer}번입니다.")

        raw_score = round(correct_count / total * 100)
        score = max(0, raw_score - hint_count * 10)
        print("\n" + "=" * 44)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if hint_count:
            print(f"💡 힌트 {hint_count}회 사용으로 {hint_count * 10}점을 차감했습니다.")
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        self.history.append(
            {
                "played_at": datetime.now().isoformat(timespec="seconds"),
                "question_count": total,
                "correct_count": correct_count,
                "score": score,
            }
        )
        self.save()

    def run(self) -> None:
        print(f"\n📂 {self.load_message}")
        try:
            while self.running:
                self.show_menu()
                choice = self.ask_number("선택: ", 1, 6)
                if choice == 1:
                    self.play_quizzes()
                elif choice == 3:
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
