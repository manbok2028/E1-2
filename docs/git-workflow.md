# Git 작업 기록

## 완료한 로컬 기록

```powershell
git init -b main
git add <기능 파일>
git commit -m "feat: ..."
git checkout -b feature/play-quiz
# 퀴즈 풀기 기능 구현 후 커밋
git checkout main
git merge --no-ff feature/play-quiz -m "merge: integrate quiz play feature branch"
git log --oneline --graph --all
```

`06-git-graph.png`에서 `feature/play-quiz` 브랜치가 main에 병합된 모습을 확인할 수 있다.

## 실제 완료한 clone·pull 실습 (2026-11-09)

```powershell
# 별도 폴더로 원격 저장소 복제
git clone https://github.com/manbok2028/E1-2.git quiz-evidence-clone

# 복제본에서 README 한 줄 변경 후 commit, push
cd quiz-evidence-clone
git add README.md
git commit -m "docs: record clone practice"
git push origin main

# 원래 E1-2 폴더에서 원격 변경 가져오기
cd ..\E1-2
git pull origin main
```

GitHub 로그인·원격 생성이 필요한 단계이므로 토큰·비밀번호·개인키는 문서나 저장소에 기록하지 않는다.

### 실제 확인 결과

```text
Cloning into 'quiz-evidence-clone'...
16cf8ce docs: add learner-friendly evaluation report and evidence

af71846 docs: record clone practice
To https://github.com/manbok2028/E1-2.git
   16cf8ce..af71846  main -> main

Updating 16cf8ce..af71846
Fast-forward
README.md | 2 ++
```

복제본에서 README에 “Git clone 실습 확인” 문장을 추가해 커밋·푸시했고, 원래 E1-2 폴더에서 `git pull origin main`으로 그 문장이 실제로 반영된 것을 확인했다.
