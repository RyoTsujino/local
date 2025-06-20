@echo off
echo Starting Backend Server...
echo.

REM プロジェクトのルートディレクトリに移動
cd /d "C:\work\order-management-system\backend"

REM 仮想環境を有効化
call venv\Scripts\activate.bat

REM 依存パッケージがインストールされているか確認（初回のみ必要）
if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM サーバーを起動
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload

pause 