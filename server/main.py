from fastapi import FastAPI
from server.routes import users, equipment, admin

app = FastAPI(title="Equipment Loan API")

app.include_router(users.router)
app.include_router(equipment.router)
app.include_router(admin.router)
