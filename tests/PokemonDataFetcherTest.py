import unittest
from unittest.mock import patch
import json
from app import PokemonDataFetcher
from app import Utils
from app.Models import Pokemon
from typing import Dict

def getAttackData(path: str) ->tuple[int, Dict| None] :
    with open("./test-data/attack.json", "r") as stat_file:
        return 200, json.load(stat_file)

def getSpecialAttackData(path: str) ->tuple[int, Dict| None] :
    with open("./test-data/special-attack.json", "r") as stat_file:
        return 200, json.load(stat_file)


def getAttackData(path: str) ->tuple[int, Dict| None] :
    with open("./test-data/attack.json", "r") as stat_file:
        return 200, json.load(stat_file)

def getPokemonData(path: str) ->tuple[int, Dict| None] :
    with open("./test-data/bubsaur.json", "r") as bubsaur_file:
        return 200, json.load(bubsaur_file)


class PokemonDataFetcherTest(unittest.TestCase):
    def test_load_cached_attack_moves(self):
        with unittest.mock.patch('app.Utils.get', getAttackData):
            attack_moves = PokemonDataFetcher.attack_moves()
            self.assertIsNotNone(attack_moves)
            self.assertEqual(45, len(attack_moves))
            self.assertEqual(-1, attack_moves["breaking-swipe"])
            self.assertEqual(2, attack_moves["shell-smash"])

    def test_load_cached_special_attack_moves(self):
        with unittest.mock.patch('app.Utils.get', getSpecialAttackData):
            attack_moves = PokemonDataFetcher.attack_special_moves()
            self.assertIsNotNone(attack_moves)
            self.assertEqual(41, len(attack_moves))
            self.assertEqual(-1, attack_moves["skitter-smack"])
            self.assertEqual(1, attack_moves["growth"])
    
    def test_load_pokemon_bubsaur(self):
        with unittest.mock.patch('app.Utils.get', getPokemonData):
            pokemon: Pokemon = PokemonDataFetcher.get_pokemon("bubsaur")
            self.assertIsNotNone(pokemon)
            self.assertEqual("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png",pokemon.image)
            self.assertEqual(6, len(pokemon.attack_moves))
            self.assertEqual(5, len(pokemon.special_attack_moves))
            self.assertEqual(65, pokemon.special_attack)
            self.assertEqual(49, pokemon.attack)
            self.assertEqual(45, pokemon.hp)
            self.assertEqual(45, pokemon.speed)

