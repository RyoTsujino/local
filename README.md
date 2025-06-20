# Order Management System

注文管理システム - FastAPIバックエンドとReactフロントエンドで構成されたWebアプリケーション

## プロジェクト構成

```
order-management-system/
├── backend/          # FastAPI バックエンド
│   ├── app/         # アプリケーションコード
│   ├── requirements.txt
│   └── main.py
└── frontend/        # React フロントエンド
    ├── src/
    ├── package.json
    └── public/
```

## セットアップ

### バックエンド（FastAPI）

1. バックエンドディレクトリに移動
```bash
cd backend
```

2. 仮想環境を作成・アクティベート
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 依存関係をインストール
```bash
pip install -r requirements.txt
```

4. サーバーを起動
```bash
uvicorn main:app --reload
```

### フロントエンド（React）

1. フロントエンドディレクトリに移動
```bash
cd frontend
```

2. 依存関係をインストール
```bash
npm install
```

3. 開発サーバーを起動
```bash
npm start
```

## 使用方法

- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:3000
- API ドキュメント: http://localhost:8000/docs

## 機能

- ユーザー認証・認可
- 注文管理
- Amazon API連携
- 管理ダッシュボード

## 開発

### Git ワークフロー

1. 新しい機能ブランチを作成
```bash
git checkout -b feature/new-feature
```

2. 変更をコミット
```bash
git add .
git commit -m "Add new feature"
```

3. プッシュ
```bash
git push origin feature/new-feature
```

## 環境変数

バックエンドで必要な環境変数は `.env` ファイルで管理してください。
参考: `backend/env_example.txt`

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 