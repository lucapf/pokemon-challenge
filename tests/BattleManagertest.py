import unittest
from unittest.mock import patch
from app import BattleManager
from app.Models import Pokemon

class BattleManagerTest(unittest.TestCase):

 def test_choose_attacker(self):
    cycles = 1000
    error = 0.01
    count = 0
    pokemon1 = Pokemon()
    pokemon1.name = 1
    pokemon1.speed = 100
    pokemon2 = Pokemon()
    pokemon2.name = 2
    pokemon2.speed = 10
    for _ in range(cycles):
        attacker = BattleManager.choose_attacker(pokemon1, pokemon2)
        if attacker == pokemon1:
            count += 1
    print("count: {count} cycles: {cycles} pokemon2.speed: {pokemon2.speed} pokemon1.speed: {pokemon1.speed}")
    self.assertTrue(abs(count/cycles - (pokemon2.speed/(pokemon1.speed + pokemon2.speed) )) < error)

    
