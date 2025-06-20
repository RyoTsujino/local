@echo off
echo Starting Both Backend and Frontend Servers...
echo.

REM 新しいウィンドウでバックエンドサーバーを起動
start "Backend Server" cmd /k "cd /d C:\work\order-management-system\backend && call venv\Scripts\activate.bat && uvicorn main:app --reload"

REM 少し待ってからフロントエンドサーバーを起動
timeout /t 3 /nobreak >nul

REM 新しいウィンドウでフロントエンドサーバーを起動
start "Frontend Server" cmd /k "cd /d C:\work\order-management-system\frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul 