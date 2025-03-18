from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import PokemonDataFetcher
from app.Models import Pokemon
import requests
from app import BattleManager
from app.BattleManager import NotValidPokemonError
from dotenv import load_dotenv, find_dotenv

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name="static")

templates = Jinja2Templates(directory="templates")

base_url = "https://pokeapi.co/api/v2/"
env_file = find_dotenv(".env")
load_dotenv(env_file)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
            request = request, name="index.html"
            )
       

@app.get("/api/v1/pokemon/{name}", response_class=HTMLResponse)
async def pokemon(name: str, request: Request, response: Response):
    pokemon:Pokemon = PokemonDataFetcher.get_pokemon(name) 
    if pokemon is None:
        response.status_code = status.HTTP_404_NOT_FOUND 
        return
    return templates.TemplateResponse (
            request = request, name="pokemon-card.html", context={"pokemon": pokemon, 
                                                                  "attacks": PokemonDataFetcher.attack_moves(), 
                                                                  "special_attacks": PokemonDataFetcher.attack_special_moves(),
                                                                  "defense": PokemonDataFetcher.defense_moves(),
                                                                  "special_defense": PokemonDataFetcher.defense_special_moves()
                                                                  }
        )

@app.post("/api/v1/battle", status_code=201, response_class=HTMLResponse)
async def battle(request: Request, response: Response):
    data = await request.json()
    print(data)
    try:
        winner, attack_items = BattleManager.attack(data["pokemon1"], data["pokemon2"])
    except NotValidPokemonError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
    return templates.TemplateResponse (
            request = request, name="battle-result.html", context={"winner": winner, 
                                                            "attacks": attack_items,
                                                            "pokemon1": data["pokemon1"],
                                                            "pokemon2": data["pokemon2"]
                                                            }
        )

    