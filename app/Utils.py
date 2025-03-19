from typing import Dict 
import requests

base_url = "https://pokeapi.co/api/v2"

def get(path: str) ->tuple[int, Dict| None] :
    """call the api using the base path, return dic if 2xxx or none"""
    resp = requests.get(f"{base_url}{path}")
    if resp.status_code == 200:
        return 200, resp.json()
    return resp.status_code, None

class InvalidPokemonNameError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def validate_pokemon_name(name:str):
    if name is None:
        raise InvalidPokemonNameError("Name cannot be None")
    if not name.replace("-","").isalnum():
        raise InvalidPokemonNameError("Name must be alphanumeric or -")
    if len(name) > 50:
        raise InvalidPokemonNameError("Name must be less than 50 characters")
