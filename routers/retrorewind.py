from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import aiohttp
import json
import os

router = APIRouter(prefix="/rr", tags=["Retro Rewind"])
#speichern der Spieler
DATA_FILE = "/app/data/players.json"

#definieren, wie die daten aussehen sollen
class Player(BaseModel):
    name: str
    fc: str

def load_players():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_players(data):
    #erstellen von app/data falls keiner da
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@router.post("/register")
def register_player(player: Player):
    players = load_players()
    #entfernen der Bindestriche für einheitlich
    fc = player.fc.replace("-", "")

    if fc not in players:
        players[fc] = {"name": player.name, "vr": 5000, "status": "offline"}
    else:
        players[fc]["name"] = player.name

    save_players(players)
    return {"message": f"{player.name} wurde erfolgreich registriert!"}

@router.get("/leaderboard")
async def get_leaderboard():
    players = load_players()
    if not players:
        raise HTTPException(status_code=404, detail="Noch keine Spieler registriert...")

    #daten abrufen
    rr_api_url = "http://rwfc.net/api/groups"
    rr_data =  []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(rr_api_url) as resp:
                if resp.status == 200:
                    rr_data = await resp.json()
    except Exception as e:
        print(f"Fehler beim Aufrufen der RR API: {e}")

    #alle Spieler auf offline setzen
    for fc in players:
        players[fc]["status"] = "offline"

    #durchsuchen der Live-Räume nach auf Server registrierten Server
    if rr_data:
        for room in rr_data:
            if "players" in room:
                for p in room["players"]:
                    #API nennt Friend Code fc
                    fc = str(p.get("fc", "")).replace("-", "")
                    if fc in players:
                        #ev ist bei WFC interne Name für VR
                        vr = p.get("ev", players[fc]["vr"])

                        #Werte updaten
                        players[fc]["vr"] = vr
                        players[fc]["status"] = "online"
                        #aktuellen Ingame Namen übernehmen
                        players[fc]["name"] = p.get("name", players[fc]["name"])

    #neue VR speichern
    save_players(players)

    #für die Ausgabe in Liste umwandeln und sortieren
    leaderboard = []
    for fc, data in players.items():
        leaderboard.append({
            "fc": fc,
            "name": data["name"],
            "vr": data["vr"],
            "status": data["status"],
        })

    #nach VR sortieren (höchste zuerst)
    leaderboard.sort(key=lambda x: x["vr"], reverse=True)
    return {"leaderboard": leaderboard}