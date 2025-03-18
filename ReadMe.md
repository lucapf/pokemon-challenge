
# Pokémon Battle field - 48 hours

## Description

Implement and code a program that receives the names of 2 pokemons and simulates a battle between the two, the winner will be decided by a calculation of the stats.change field.

In addition to this, you should show each pokemons ID card (general information) by fetching data from the pokeapi.co for each given name .

- Use models for the pokemons
- The program should handle errors.
- The program should have a cache mechanism.
- Use Docker containers
- All battle data should be saved in a DB (up to you which db to use)
- The project should include unit tests and documentation.

https://pokeapi.co/

## pokemon selection

### base flow

1. The operator insert the name of the pokemon
2. the system checks if the pokemon exists.
3. fetch the pokemon data and shown basic information (name, image (generation-viii then back), HP points, attack and defense moves ).
4. the operator choose the second pokemon. The system operarate following the same process

#### alternative 1

1 as  base flow
2. pokemon not found --> the system shown a message `sorry I cannot find the pokemon <name> try again`
3. ask for a new pokemon name

## Battle

1. the operator press the "battle" button
2. checks if both pokemon have attack and defense moves in the arsenal
3. the system:
    1. randomly choose one of the pokemon as attacker
    2. randomly choose one of the attack move for the attacker
    3. randomly choose one of the defense moves for the defender
    4. calcolate the damage for both as `effort` for the attacker and `attack.change - defense.change` for the defender
    5. if hp > 0 for both restart for the point 2
4. the first pokemon with hp = 0 loose the battle

The system store all steps of the battle in a database

## List battels

as an operator I want be able to see the list of past battels shown by the system in cronological order newest to oldest.
The system shown:

1. date and time of battel, pokemon names and how win
2. selecting the row, the system reply with all steps with scores

## Data structures

### Pokemon model
