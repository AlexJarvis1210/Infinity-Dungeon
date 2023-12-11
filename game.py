from classes import *
from functions import *
import sys
import time
import re
import random
from tabulate import tabulate

def main():

    f = Figlet(font="slant")
    print(f.renderText("Welcome to the Infinity Dungeon!"))

    # Create the player character
    player_1 = create_character()

    # Instantiate a random room
    room_1 = generate_room()

    # Instantiate enemies based on nuber of enemies in the room
    room_1.enemies = [generate_enemy(player_1.level) for _ in range(room_1.number_of_enemies)]

    # Print the room description
    type_out(f"{player_1.name} enters a {room_1.description}.")

    # Print the enemies description
    if room_1.number_of_enemies == 1:
        type_out(f"{player_1.name} sees a {room_1.enemies[0].name} standing in the corner and studies the enemy...")
        type_out(str(room_1.enemies[0]))
    else:
        type_out(f"{player_1.name} sees {room_1.number_of_enemies} enemies standing in the corner and studies them...")
        for enemy in room_1.enemies:
            type_out(f"{enemy.name}:")
            type_out(str(enemy))

    game_loop(player_1, room_1)


if __name__ == "__main__":
    main()


