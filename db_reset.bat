@echo off
title Build DB Reset Tool
color 0A

echo ============================================
echo   Build Number Manager - DB 초기화 도구
echo ============================================
echo.

REM 경로 설정
SET PROJECT_DIR=C:\Users\hyuck\Documents\빌드관리페이지
SET DB_FILE=%PROJECT_DIR%\database\build.db

echo ■ 서버 프로세스 종료 중...
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM uvicorn.exe /F >nul 2>&1
taskkill /IM uvicorn /F >nul 2>&1
echo 완료!
echo.

echo ■ 기존 DB 삭제 중...
if exist "%DB_FILE%" (
    del "%DB_FILE%"
    echo build.db 삭제 완료!
) else (
    echo build.db 파일이 존재하지 않습니다. (이미 초기화됨)
)
echo.

echo ■ 서버 재시작 중...
cd "%PROJECT_DIR%"
start cmd /k "uvicorn backend.main:app --reload"

echo.
echo ============================================
echo   🔥 DB 초기화 & FastAPI 서버 재시작 완료!
echo ============================================
echo.
pause
