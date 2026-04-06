from fastapi import FastAPI
from app.api.v1 import auth, users, transactions, dashboard

app = FastAPI(title="Finance Backend", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "Welcome to the Finance Backend API"}