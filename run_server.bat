@echo off
echo ==============================================
echo   🚀 Build Management Server Starting...
echo ==============================================
echo.

REM 1) 프로젝트 폴더로 이동
cd /d C:\Users\hyuck\Documents\빌드관리페이지

REM 2) 서버 실행
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

pause
