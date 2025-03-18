from typing import Dict 
import requests

base_url = "https://pokeapi.co/api/v2"
def get(path: str) ->tuple[int, Dict| None] :
    """call the api using the base path, return dic if 2xxx or none"""
    resp = requests.get(f"{base_url}{path}")
    if resp.status_code == 200:
        return 200, resp.json()
    return resp.status_code, None
