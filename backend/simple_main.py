from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Order Management System", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Order Management System API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.get("/api/orders")
async def get_orders():
    # サンプルデータ
    return {
        "orders": [
            {"id": 1, "customer": "田中太郎", "product": "商品A", "quantity": 2, "status": "処理中"},
            {"id": 2, "customer": "佐藤花子", "product": "商品B", "quantity": 1, "status": "完了"},
            {"id": 3, "customer": "鈴木一郎", "product": "商品C", "quantity": 3, "status": "待機中"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 