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

## 원격 제출 뒤 실제로 수행할 clone·pull 실습

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
