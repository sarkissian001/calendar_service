from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import events

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

# https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)


@app.get("/")
async def main():
    return {"message": "Welcome To Calendar Service"}
