"""생활세금 퀴즈 게임 실행 파일."""

import sys

from game import QuizGame


def configure_console() -> None:
    """Windows 콘솔에서도 한글·이모지 안내가 깨지지 않도록 UTF-8을 사용한다."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    configure_console()
    QuizGame().run()
