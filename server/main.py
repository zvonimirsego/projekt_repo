from fastapi import FastAPI
from server.routes import users

app = FastAPI(
    title="Equipment Loan API"
)

app.include_router(users.router)