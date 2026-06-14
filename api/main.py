from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database import db

app = FastAPI(title="Blackwood Poker Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    nickname: str

class TournamentCreate(BaseModel):
    title: str
    date: str
    time: str
    max_players: int = 40
    reentry_cost: int = 1500
    addon_cost: int = 3000

class RegisterRequest(BaseModel):
    tournament_id: int
    user_id: int

class ResultInput(BaseModel):
    tournament_id: int
    user_id: int
    place: int
    reentries: int = 0

@app.on_event("startup")
def startup():
    db.init_db()

@app.get("/")
def root():
    return {"message": "Blackwood Poker Club API", "status": "running"}

@app.post("/users")
def create_user(user: UserCreate):
    user_id = db.add_user(user.telegram_id, user.username, user.nickname)
    if not user_id:
        raise HTTPException(status_code=400, detail="Nickname or Telegram ID already exists")
    return {"id": user_id, "message": "User created"}

@app.get("/users/{telegram_id}")
def get_user(telegram_id: int):
    user = db.get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/tournaments")
def list_tournaments(status: Optional[str] = None):
    return db.get_tournaments(status)

@app.post("/tournaments")
def create_tournament(t: TournamentCreate):
    tid = db.create_tournament(t.title, t.date, t.time, t.max_players, t.reentry_cost, t.addon_cost)
    return {"id": tid, "message": "Tournament created"}

@app.get("/tournaments/{tournament_id}")
def get_tournament(tournament_id: int):
    t = db.get_tournament(tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    t["registrations"] = db.get_registrations(tournament_id)
    t["registered_count"] = db.get_registration_count(tournament_id)
    return t

@app.post("/register")
def register(req: RegisterRequest):
    if db.is_registered(req.tournament_id, req.user_id):
        raise HTTPException(status_code=400, detail="Already registered")
    t = db.get_tournament(req.tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if db.get_registration_count(req.tournament_id) >= t["max_players"]:
        raise HTTPException(status_code=400, detail="Tournament is full")
    db.register_user(req.tournament_id, req.user_id)
    return {"message": "Registered successfully"}

@app.post("/unregister")
def unregister(req: RegisterRequest):
    db.unregister_user(req.tournament_id, req.user_id)
    return {"message": "Unregistered"}

@app.post("/results")
def add_result(res: ResultInput):
    points = db.add_result(res.tournament_id, res.user_id, res.place, res.reentries)
    return {"points": points, "message": "Result recorded"}

@app.get("/leaderboard")
def leaderboard():
    return db.get_leaderboard()

@app.get("/users/{user_id}/stats")
def user_stats(user_id: int):
    return db.get_user_stats(user_id)

@app.get("/users/{user_id}/achievements")
def user_achievements(user_id: int):
    return db.get_user_achievements(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
