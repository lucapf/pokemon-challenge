import unittest
from unittest.mock import patch
import json
from app import PokemonDataFetcher
from app import Utils
from tests import UtilsTest
from app.Models import Pokemon
from typing import Dict


class PokemonDataFetcherTest(unittest.TestCase):
    def test_load_cached_attack_moves(self):
        with unittest.mock.patch('app.Utils.get', UtilsTest.get_static_data):
            attack_moves = PokemonDataFetcher.attack_moves()
            self.assertIsNotNone(attack_moves)
            self.assertEqual(45, len(attack_moves))
            self.assertEqual(-1, attack_moves["breaking-swipe"])
            self.assertEqual(2, attack_moves["shell-smash"])

    def test_load_cached_special_attack_moves(self):
        with unittest.mock.patch('app.Utils.get',UtilsTest.get_static_data): 
            attack_moves = PokemonDataFetcher.attack_special_moves()
            self.assertIsNotNone(attack_moves)
            self.assertEqual(41, len(attack_moves))
            self.assertEqual(-1, attack_moves["skitter-smack"])
            self.assertEqual(1, attack_moves["growth"])
    
    def test_load_pokemon_bubsaur(self):
        with unittest.mock.patch('app.Utils.get',UtilsTest.get_static_data): 
            pokemon: Pokemon = PokemonDataFetcher.get_pokemon("bubsaur")
            self.assertIsNotNone(pokemon)
            self.assertEqual("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png",pokemon.image)
            self.assertEqual(6, len(pokemon.attack_moves))
            self.assertEqual(5, len(pokemon.special_attack_moves))
            self.assertEqual(65, pokemon.special_attack)
            self.assertEqual(49, pokemon.attack)
            self.assertEqual(45, pokemon.hp)
            self.assertEqual(45, pokemon.speed)

    def test_if_pokemon_name_is_not_valid_then_InvalidPokemonNameError_occur(self):
        with self.assertRaises(Utils.InvalidPokemonNameError) as context:
            PokemonDataFetcher.get_pokemon("bubsauri-1~")
        self.assertEqual("Name must be alphanumeric or -",str(context.exception))
        try:
            PokemonDataFetcher.get_pokemon("12bUbsauri-1")
        except Utils.InvalidPokemonNameError as context:
            self.fail("should not raise an exception")

