from typing import List

class Pokemon(object):
    def __init__(self):
        self.name: str 
        self.image: str
        self.attack_moves: List[Move] = list()
        self.special_attack_moves: List[Move] = list()
        self.defense_moves: List[Move] = list()
        self.special_defense_moves: List[Move] = list()
        self.hp: int
        self.speed: int
        self.attack: int
        self.special_attack: int


class Move(object):
    def __init__(self, name: str, target_attack_change: int, attacker_attack_change: int ): 
        self.name: str = name 
        self.target_attack_change: int = target_attack_change 
        self.attacker_attack_change: int =  attacker_attack_change 


class Attack(object):
    def __init__(self, battle_id: int, attacker: str, pokemon_1_hp: int,pokemon_2_hp: int ,
                 attack_move: str , defense_move: str , attack_damage: int, defense_damage: int):
        self.battle_id: int = battle_id
        self.attacker: Pokemon = attacker
        self.pokemon_1_hp: int = pokemon_1_hp 
        self.pokemon_2_hp: int = pokemon_2_hp 
        self.attack_move: str = attack_move
        self.defense_move: str = defense_move
        self.attack_damage: int = attack_damage
        self.defense_damage: int = defense_damage