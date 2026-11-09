# E1-2 · 우리 문화 퀴즈 게임

Python으로 만든 터미널 퀴즈 게임입니다. 퀴즈를 풀고 직접 추가할 수 있으며, 프로그램을 껐다 켜도 퀴즈·최고 점수·게임 이력이 `state.json`에 남습니다.

> Git clone 실습 확인: 2026-11-09에 별도 폴더로 복제한 뒤 이 문장을 추가하고 원격에 푸시했습니다.

- 평가자를 위한 쉬운 설명: [평가 보고서](docs/evaluation-report.md)
- Git 브랜치·병합·원격 실습 기록: [Git 작업 기록](docs/git-workflow.md)
- 실제 실행 PNG: [docs/screenshots](docs/screenshots)

## 퀴즈 주제와 선정 이유

한글, 무궁화, 독도처럼 우리 문화와 태양·무지개 같은 기초 과학을 주제로 골랐습니다. 이미 알고 있는 소재를 이용하면 “문제 맞히기”에만 집중하지 않고 Python의 입력·조건·반복·파일 저장을 자연스럽게 배울 수 있습니다. 기본 퀴즈는 6개이며, 사용자가 더 추가할 수 있습니다.

## 실행 방법

Python 3.10 이상이 필요합니다. 게임 자체는 **외부 라이브러리를 사용하지 않습니다.**

```powershell
cd E1-2
python main.py
```

테스트는 다음 명령으로 실행합니다.

```powershell
python -m unittest discover -s tests -v
```

## 기능 목록

1. 무작위 퀴즈 출제와 문제 수 선택
2. 정답·오답 안내, 최고 점수와 게임 이력 저장
3. 힌트 보기와 힌트당 10점 감점 (보너스)
4. 새 퀴즈 등록과 즉시 저장
5. 퀴즈 목록 보기
6. 퀴즈 삭제와 저장 (보너스)
7. 빈 입력·문자·범위 밖 숫자 안내 및 재입력
8. 파일 없음·손상·읽기/쓰기 오류와 Ctrl+C·EOF 안전 처리

## 파일 구조

```text
E1-2/
├── main.py                 # 프로그램 시작점과 Windows UTF-8 콘솔 설정
├── game.py                 # QuizGame: 메뉴, 플레이, 추가, 목록, 점수, 삭제
├── quiz.py                 # Quiz: 문제 한 개의 구조와 채점
├── default_data.py         # 기본 퀴즈 6개
├── storage.py              # UTF-8 JSON 저장·불러오기·복구
├── state.json              # 실제 퀴즈, 최고 점수, 게임 이력
├── tests/                  # 표준 라이브러리 unittest 테스트
├── docs/                   # 평가 보고서, Git 기록, 실제 실행 PNG
└── scripts/                # PNG 증빙 재생성 보조 도구
```

## 데이터 파일 설명

`state.json`은 프로젝트 루트에 있으며 UTF-8 JSON 형식입니다.

```json
{
  "quizzes": [
    {"question": "문제", "choices": ["선택지1", "선택지2", "선택지3", "선택지4"], "answer": 1, "hint": "힌트"}
  ],
  "best_score": 0,
  "history": [{"played_at": "2026-11-09T12:00:00", "question_count": 1, "correct_count": 1, "score": 100}]
}
```

- 파일이 없으면 기본 퀴즈 데이터를 사용합니다.
- 파일이 손상됐으면 안내를 출력하고 기본 데이터로 복구합니다.
- 저장 오류가 발생해도 프로그램이 갑자기 멈추지 않도록 처리합니다.
