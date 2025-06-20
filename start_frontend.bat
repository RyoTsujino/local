@echo off
echo Starting Frontend Server...
echo.

REM プロジェクトのフロントエンドディレクトリに移動
cd /d "C:\work\order-management-system\frontend"

REM node_modulesが存在しない場合は依存パッケージをインストール
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

REM 開発サーバーを起動
echo Starting React development server...
echo Server will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
npm start

pause 