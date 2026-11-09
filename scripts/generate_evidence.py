"""실제 콘솔 실행 출력과 Git 로그를 PNG 증빙으로 만드는 보조 도구.

퀴즈 게임 본체는 외부 라이브러리 없이 동작한다. 이 파일은 제출용 PNG 생성에만
Pillow를 사용하며, 게임의 실행 환경에는 필요하지 않다.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "screenshots"
FONT_PATH = Path("C:/Windows/Fonts/malgun.ttf")


def command_output(command: list[str], user_input: str = "") -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        input=user_input,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return (result.stdout + result.stderr).strip()


def render_terminal(filename: str, title: str, text: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(FONT_PATH), 22)
    title_font = ImageFont.truetype(str(FONT_PATH), 25)
    lines = text.splitlines() or ["(출력이 없습니다)"]
    width = 1450
    height = max(300, 100 + len(lines) * 34)
    image = Image.new("RGB", (width, height), "#121826")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 58), fill="#263247")
    draw.ellipse((22, 18, 36, 32), fill="#ff6b6b")
    draw.ellipse((44, 18, 58, 32), fill="#ffd166")
    draw.ellipse((66, 18, 80, 32), fill="#4cd97b")
    draw.text((108, 14), title, font=title_font, fill="#f8fafc")
    y = 78
    for line in lines:
        draw.text((28, y), line, font=font, fill="#dce8f6")
        y += 34
    image.save(OUTPUT / filename)


def main() -> None:
    python = sys.executable
    environment = command_output([python, "--version"]) + "\n" + command_output(["git", "--version"])
    render_terminal("01-environment.png", "개발 환경 확인", environment)

    menu = command_output([python, "main.py"], "6\n")
    render_terminal("02-menu-and-exit.png", "실제 프로그램 실행 · 메뉴와 안전한 종료", menu)

    invalid = command_output([python, "main.py"], "abc\n9\n6\n")
    render_terminal("03-invalid-input.png", "실제 프로그램 실행 · 잘못된 입력 처리", invalid)

    add_and_list = command_output(
        [python, "main.py"],
        "2\nWhat is the English word for water?\nwater\nfire\nwind\nearth\n1\nWater hint\n3\n6\n",
    )
    render_terminal("04-add-and-list.png", "실제 프로그램 실행 · 퀴즈 추가와 목록", add_and_list)

    play = command_output([python, "main.py"], "1\n1\n1\n6\n")
    render_terminal("05-play-and-score.png", "실제 프로그램 실행 · 퀴즈 풀기", play)

    git_log = command_output(["git", "log", "--oneline", "--graph", "--all"])
    render_terminal("06-git-graph.png", "Git 커밋과 브랜치 병합 기록", git_log)


if __name__ == "__main__":
    main()
