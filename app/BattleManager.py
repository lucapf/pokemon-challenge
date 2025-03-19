import psycopg2 as psycopg
import os
from psycopg import Connection
from app.Models import Pokemon, Attack
from app import PokemonDataFetcher
import random
import copy
from typing import List

class NotValidPokemonError(Exception):

    def __init__(self, message: str ):
        super().__init__(message)
        self.message = message


def _connect():
    database_name = os.getenv("DBNAME")
    host = os.getenv("PG_HOST")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    port = os.getenv("PG_PORT")
    
    print(f"connecting to {database_name} on {host}:{port} as {user}")
    conn = psycopg.connect(dbname=database_name,
                        host=host,
                        user=user,
                        password=password,
                        port=port)
    return conn 

def save_start_battle(pokemon1:Pokemon, pokemon2:Pokemon, conn: Connection) -> int:
    """save the start of the battle in the database"""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO public.battle (pokemon_1, pokemon_2,initial_hp_1, initial_hp_2) VALUES (%s, %s, %s, %s) returning id", \
                (pokemon1.name, pokemon2.name,pokemon1.hp, pokemon2.hp))
        return cur.fetchone()[0]

def end_game(conn:Connection, battle_id: int, winner: str|None):
    with conn.cursor() as cur:
        cur.execute("UPDATE public.battle SET winner = %s, end_date = now() WHERE id = %s", (winner, battle_id))

def save_attack(attack: Attack, conn: Connection) :
    with conn.cursor() as cur:
        cur.execute("INSERT INTO attack(battle_id, pokemon_1_hp, pokemon_2_hp,attacker," \
                    "attack_move, defense_move , attack_damage, defense_damage)" \
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", \
                (attack.battle_id, attack.pokemon_1_hp, 
                 attack.pokemon_2_hp, attack.attacker, attack.attack_move,attack.defense_move, attack.attack_damage, attack.defense_damage))

def choose_attacker(pokemon1:Pokemon, pokemon2:Pokemon) -> {Pokemon, Pokemon}:
    """choose the attacker, the one with the highest speed have more chance to attack first"""
    threshold = pokemon1.speed / (pokemon1.speed + pokemon2.speed)
    value = random.random()
    attacker= pokemon1 if random.random() < threshold else pokemon2
    return attacker 

def choose_special_attack(attacker: Pokemon, defender:Pokemon) -> bool:
    """choose if the attacker will use a special attack or not"""
    special_attack_factor = len(attacker.special_attack_moves) / (len(attacker.special_attack_moves) + len(attacker.attack_moves))
    speed_factor=attacker.speed / (attacker.speed + defender.speed)
    return random.random() < (special_attack_factor * speed_factor) 

def choose_special_defense(attacker: Pokemon, defender:Pokemon) -> bool:
    """choose if the attacker will use a special attack or not(same as special attack)"""
    special_defense_factor = len(defender.special_defense_moves) / (len(defender.special_defense_moves) + len(defender.defense_moves))
    speed_factor=defender.speed / (defender.speed + defender.speed)
    return random.random() < (special_defense_factor * speed_factor) 


def setup_battle(p1:str|None, p2:str|None) -> {Pokemon|None, Pokemon|None}:
    """start the battle between two pokemons, return:
    error_message: str|None: if not None then an error occured
    pokemon1: Pokemon|None: the first pokemon object
    pokemon2: Pokemon|None: the second pokemon object
    attacker: Pokemon|None: the pokemon that will attack first
    """
    if p1 is None or  p2 is None:
        raise NotValidPokemonError("you must specify pokemon1 and pokemon2 names")
    if p1 == p2:
        raise NotValidPokemonError("cannot battle the same pokemon")
    pokemon1 = PokemonDataFetcher.get_pokemon(p1)
    pokemon2 = PokemonDataFetcher.get_pokemon(p2)
    if pokemon1 is None or pokemon2 is None:
        raise NotValidPokemonError("cannot find one of the pokemon, pls check the names and try again")
    if len(pokemon1.attack_moves) == 0 or len(pokemon2.attack_moves) == 0:
        raise NotValidPokemonError("one of the pokemon has no attack moves")
    if pokemon1.hp == 0 or pokemon2.hp == 0:
        raise NotValidPokemonError("one of the pokemon has no hp")
    return copy.copy(pokemon1), copy.copy(pokemon2)

def choose_attak_move(attacker: Pokemon, special_attack: bool) -> str:
    """choose the attack move that the attacker will use"""
    return random.choice(     attacker.special_attack_moves if special_attack\
                         else attacker.attack_moves)
                         
def choose_defense_move(attacker: Pokemon, special_attack: bool) -> str:
    """choose the attack move that the attacker will use"""
    return random.choice(     attacker.special_defense_moves if special_attack\
                         else attacker.defense_moves)


def attack(p1: str, p2:str) -> {str, List[Attack]}:
    """"
    emulate the battle.
    Iterate until one of the pokemon hp is 0
    save the battle in the database
    """
    attack_moves: List[Attack] = list()
    pokemon1, pokemon2 = setup_battle(p1, p2)
    with _connect() as conn:
        battle_id = save_start_battle(pokemon1, pokemon2, conn)
        count = 0
        while pokemon1.hp > 0 and pokemon2.hp > 0 and count < 200:
            count += 1
            attacker = choose_attacker(pokemon1, pokemon2)
            defender = pokemon2 if attacker.name == pokemon1.name else pokemon1
            special_attack = choose_special_attack(attacker, defender)
            attack_move = choose_attak_move(attacker, special_attack)
            if special_attack:
                attack_change = PokemonDataFetcher.attack_special_moves()[attack_move]
            else:
                attack_change = PokemonDataFetcher.attack_moves()[attack_move]
            defender.hp += attack_change if attack_change < 0 else 0 # decrease affects hp only
            special_defence = choose_special_defense(defender, attacker)
            defense_move = choose_defense_move(attacker, special_defence)
            if special_defence:
                defense_change = PokemonDataFetcher.defense_special_moves()[defense_move] 
            else:
                defense_change = PokemonDataFetcher.defense_moves()[defense_move]
            attacker.hp += defense_change if defense_change < 0 else 0 # decrease  affect hp only
            attack_moves.append(Attack(battle_id, attacker.name, 
                                       pokemon1.hp, pokemon2.hp,
                                       attack_move, defense_move,
                                       attack_change,
                                       defense_change))
            save_attack(attack_moves[-1], conn)
        winner = pokemon1 if pokemon2.hp == 0 else pokemon2 if pokemon1.hp == 0 else None
        end_game(conn, battle_id, winner.name if winner is not None else "no winner")
        conn.commit()
        return winner.name if winner is not None else "no winner", attack_moves