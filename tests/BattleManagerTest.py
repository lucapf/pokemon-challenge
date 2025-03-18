import unittest
from unittest.mock import patch
import unittest.mock
from app.BattleManager import choose_attacker, choose_special_attack, setup_battle, NotValidPokemonError
from app.Models import Pokemon
import json
from app import Utils

def get_pokemon(path: str) ->tuple[int, dict| None] :
        if path == "/stat/2":
            with open("./test-data/attack.json", "r") as stat_file:
                return 200, json.load(stat_file)
        if path == "/stat/4":
            with open("./test-data/special-attack.json", "r") as stat_file:
                return 200, json.load(stat_file)
        name = path.split("/")[-1]
        with open(f"./test-data/{name}.json", "r") as pokemon_file:
            return 200, json.load(pokemon_file)


class BattleManagerTest(unittest.TestCase):

    def test_choose_attacker(self):
        """higher speed pokemon have more chance to attack first"""
        cycles = 100
        error = 0.07
        pokemon1  = Pokemon()
        pokemon2  = Pokemon()
        count = 0
        pokemon1.speed = 100
        pokemon2.speed = 170
        for _ in range(cycles):
            attacker = choose_attacker(pokemon1, pokemon2)
            count += 1 if attacker == pokemon1 else 0
        actual_error = abs(count/cycles - pokemon1.speed/(pokemon1.speed + pokemon2.speed))
        print(f"count: {count} cycles: {cycles} actual_error: {actual_error}")
        self.assertTrue( actual_error < error)

    def test_choose_special_attack(self):
        """
        Chances to choose a special attack is higher if the attacker has more special 
        attack moves and higher speed
        """
        cycles = 10000
        error = 0.1
        attack_moves = 100
        special_attack_moves = 10
        count = 0
        pokemon1  = Pokemon()
        pokemon2  = Pokemon()
        pokemon1.speed = 100
        pokemon2.speed = 10
        pokemon1.special_attack_moves = [i for i in range(special_attack_moves)]
        pokemon1.attack_moves = [i for i in range(attack_moves)]
        for _ in range(cycles):
            special_attack_choosed = choose_special_attack(pokemon1, pokemon2)
            count += 1 if special_attack_choosed else 0
        special_attack_factor = special_attack_moves/(special_attack_moves + attack_moves) 
        speed_factor = pokemon1.speed / (pokemon1.speed + pokemon2.speed)
        actual_error = abs(count/cycles - ( speed_factor * special_attack_factor))
        print(f"count: {count} cycles: {cycles} special_attack_factor: {special_attack_factor}" + \
               f"attack_factor: {speed_factor} speed * special attack {special_attack_factor* speed_factor} actual_error: {actual_error}")
        self.assertTrue( actual_error < error)

    def test_start_battle(self):
        with unittest.mock.patch("app.BattleManager._connect", return_value=None):
            with unittest.mock.patch("app.BattleManager.save_start_battle", return_value=None):
                with unittest.mock.patch("app.PokemonDataFetcher.get_pokemon", return_value=None):
                    try:
                        pokemon1, pokemon2 = setup_battle(None, None)
                        self.fail("should raise an exception")
                    except NotValidPokemonError as e:
                        self.assertEqual("you must specify pokemon1 and pokemon2 names",str(e))
                    try:
                        pokemon1, pokemon2 = setup_battle("ditto", "ditto")
                        self.fail("should raise an exception")
                    except NotValidPokemonError as e:
                        self.assertEqual("cannot battle the same pokemon",str(e))
                with unittest.mock.patch("app.Utils.get", get_pokemon):
                    try:
                        pokemon1, pokemon2 = setup_battle("ditto", "bubsaur")
                        self.fail("should raise an exception")
                    except NotValidPokemonError as e:
                        self.assertEqual("one of the pokemon has no attack moves",str(e))

