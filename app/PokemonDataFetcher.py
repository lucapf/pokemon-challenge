from functools import cache
from typing import Dict
from app import Utils
from app.Models import Pokemon
from app import PokemonDataFetcher

def __decode_attack_registry_moves(code: int, data: Dict) -> Dict[str,int]:
    attack_moves_dic: Dict[str,int] = dict()
    if code != 200 or data is None:
        return None
    decrease_moves = data["affecting_moves"]["decrease"]
    for i in decrease_moves:
        attack_moves_dic[str(i["move"]["name"])] =  int(i["change"]) 
    increase_moves = data["affecting_moves"]["increase"]
    for i in increase_moves:
        attack_moves_dic[str(i["move"]["name"])] =  int(i["change"]) 
    return attack_moves_dic 


@cache
def attack_moves() -> Dict[str,int]|None:
    code, data = Utils.get("/stat/2")
    return __decode_attack_registry_moves(code, data)
    
@cache
def attack_special_moves() -> Dict[str,int]|None:
    code, data = Utils.get("/stat/4")
    return __decode_attack_registry_moves(code, data)
@cache

def defense_moves() -> Dict[str,int]|None:
    code, data = Utils.get("/stat/3")
    return __decode_attack_registry_moves(code, data)
    
@cache
def defense_special_moves() -> Dict[str,int]|None:
    code, data = Utils.get("/stat/5")
    return __decode_attack_registry_moves(code, data)


@cache
def get_pokemon(name: str) -> Pokemon:
    Utils.validate_pokemon_name(name)
    code, data = Utils.get(f'/pokemon/{name}')
    if code != 200 or data is None:
        return None
    p = Pokemon()
    p.name = data["name"]
    p.image = data["sprites"]["other"]["home"]["front_default"]
    for s in data["stats"]:
        if s["stat"]["name"] == "hp":
            p.hp = s["base_stat"]
        if s["stat"]["name"] == "speed":
            p.speed = s["base_stat"]
        if s["stat"]["name"] == "attack":
            p.attack = s["base_stat"]
        if s["stat"]["name"] == "special-attack":
            p.special_attack = s["base_stat"]
    attack_moves = PokemonDataFetcher.attack_moves().keys()
    attack_special_moves = PokemonDataFetcher.attack_special_moves().keys()
    defense_moves = PokemonDataFetcher.defense_moves().keys()
    defense_special_moves = PokemonDataFetcher.defense_special_moves().keys()
    pokemon_moves = [m["move"]["name"] for m in data["moves"]]
    p.attack_moves = list(set(pokemon_moves) & set(attack_moves))
    p.special_attack_moves = list(set(pokemon_moves) & set(attack_special_moves))
    p.defense_moves = list(set(pokemon_moves) & set(defense_moves))
    p.special_defense_moves = list(set(pokemon_moves) & set(defense_special_moves))
    return p
