import json
from loguru import logger

def get_static_data(path: str) ->tuple[int, dict| None] :
        logger.debug(f"get_static_data: {path}") 
        name = path.split("/")[-2]
        if path == "/stat/1":
            name = "hp"
        elif path == "/stat/2":
            name = "attack"
        elif path == "/stat/3":
            name = "defense"
        elif path == "/stat/4":
            name = "special-attack"
        elif path == "/stat/5":
            name = "special-defense"
        elif path == "/pokemon/bubsaur":
            name = "bubsaur"
        logger.debug(f"resolved name: {name}") 
        with open(f"./test-data/{name}.json", "r") as pokemon_file:
            return 200, json.load(pokemon_file)
