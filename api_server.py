# api_server.py
from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from controllers import PlayerController
from models import Player
from typing import List
import json
import uvicorn  # type: ignore

app = FastAPI()
player_controller = PlayerController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/questions")
async def get_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    return questions


@app.post("/submit-score")
async def submit_score(player: Player):
    return player_controller.submit_score(player)


@app.get("/ranking", response_model=List[Player])
async def get_ranking():
    return player_controller.get_ranking()


def run_fastapi():
    uvicorn.run(app, host="https://serverquizapis-gvqxqkov76pqp3qpxaey97.streamlit.app/", port=8080)
