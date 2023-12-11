from classes import *
from pyfiglet import Figlet
import sys
import re
import random
from tabulate import tabulate
from utility import type_out


def create_character():
    player_1 = Character()
    valid_name = False
    while not valid_name:
        name = input("What is your character's name? ").strip()
        if re.fullmatch(r"^[A-Za-z\s]+$", name):
            player_1.name = name
            valid_name = True
        else:
            print("Invalid name. Please use only letters and spaces.")

    valid_spec = False
    available_specs = ["Rogue", "Beserker", "Knight"]
    while not valid_spec:
        spec = input(f"What spec is your character? Choose from {available_specs}: ").capitalize().strip()
        if spec in available_specs:
            player_1.spec = spec
            valid_spec = True
        else:
            print("Invalid spec. Please choose a valid spec from the list.")

    player_1.assign_default_weapon()
    return player_1


def generate_enemy(player_level):
    enemy_names = [
        "Weak Goblin",
        "Dark Iron Dwarf",
        "Flame Wizard",
        "Troll Brute",
        "Shadow Assassin",
        "Frost Archer",
        "Stone Golem",
        "Enraged Wolf",
        "Ethereal Spirit",
        "Undead Warrior"
    ]

    name = random.choice(enemy_names)
    level = random.choice(range(max(1, player_level - 1), player_level + 2))
    health = random.randint(50, 200) * (level / 2)
    strength = random.randint(10, 40) * (level / 2)
    defense = random.randint(5, 20) * (level / 2)
    speed = random.randint(5, 20) * (level / 2)
    xp_reward = random.randint(25,50) * level

    return Enemy(name, health, strength, defense, speed, level, xp_reward)

def generate_room():
    # return Room.generate_random_room()

    # Temporary code for testing purposes
    room = Room.generate_random_room()
    room.has_treasure_chest = True
    return room

def generate_treasure_chest():
    treasure_chest = {}
    weapons = [Weapon.rusty_iron_sword, Weapon.wooden_staff, Weapon.elven_bow, Weapon.orcish_warhammer,
               Weapon.dwarven_axe, Weapon.enchanted_greatsword, Weapon.fireball_scepter, Weapon.venomous_dagger,
               Weapon.divine_halberd, Weapon.diamond_encrusted_longsword]

    buffs = [
        ("health potion", "heal", random.randint(10, 50)),
        ("speed rune", "speed", random.randint(1, 5)),
        ("strength rune", "strength", random.randint(1, 5)),
        ("agility rune", "agility", random.randint(1, 5)),
        ("defense rune", "defense", random.randint(1, 5))
]

    # Randomly select a weapon with 33% probability
    if random.random() < 0.33:
        treasure_chest["weapon"] = random.choice(weapons)()

    # Randomly select buffs (1 to 3)
    num_buffs = random.randint(1, 3)
    treasure_chest["buffs"] = random.sample(buffs, num_buffs)

    return treasure_chest

def get_turn_order(player, enemy):
    if player.speed >= enemy.speed:
        print(f"{player.name} attacks first!")
        return player, enemy
    else:
        print(f"{enemy.name} attacks first!")
        return enemy, player

def player_turn(player, enemy):
    action = input("What do you want to do? (A)ttack or (I)nventory: ").lower()
    if action == "a":
        damage = player.attack(enemy)
        enemy.health -= damage  # Update enemy health
        type_out(f"You dealt {damage} damage to the {enemy.name}!")
    elif action == "i":
        player.open_inventory()
    else:
        type_out("Invalid action. Please choose '(A)ttack' or '(I)nventory'.")


def enemy_turn(player, enemy):
    type_out(f"It's {enemy.name}'s turn!")
    damage = enemy.attack(player)
    player.health -= damage  # Update player health
    type_out(f"{enemy.name} dealt {damage} damage to you!")


def combat(player, enemy, room):
    while player.health > 0 and enemy.health > 0:
        player_turn(player, enemy)  # Pass player and enemy objects
        if enemy.health <= 0:
            type_out(f"{enemy.name} is defeated!")
            room.number_of_enemies -= 1
            break
        else:
            type_out(f"{enemy.name}'s remaining health: {enemy.health}")

        enemy_turn(player, enemy)  # Pass player and enemy objects
        if player.health <= 0:
            type_out(f"{player.name} is defeated!")
            f = Figlet(font="slant")
            print(f.renderText("Game Over"))
            sys.exit()
        else:
            type_out(f"{player.name}'s remaining health: {player.health}")



def display_menu():
    f = Figlet(font="standard")
    print(f.renderText("Menu"))
    menu_options = [
        ["(A)", "Attack enemy"],
        ["(S)", "Search room"],
        ["(I)", "Inventory"],
        ["(N)", "Next room"],
        #["(P)", "Player Stats"]
        ["(Q)", "Quit"]
    ]
    print(tabulate(menu_options, tablefmt="plain"))


def game_loop(player, room):
    rooms_cleared = 0
    enemies = room.enemies
    while True:
        if player.health <= 0:
            game_over(player, rooms_cleared)
            break

        display_menu()
        choice = input("Choose an option: ").lower()

        if choice == "a":
            # Attack enemy
            if not enemies:
                type_out("There are no enemies in the room.")
            else:
                enemy = enemies[0]  # Select the first enemy
                combat(player, enemy, room)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    player.gain_xp(enemy.xp_reward)
                    type_out(f"You gained {enemy.xp_reward} XP.")
                    if not enemies:
                        type_out("All enemies in the room have been defeated!")
        elif choice == "s":
            # Search room for a treasure chest
            room.search_room(player)
        elif choice == "i":
            # Open inventory
            player.open_inventory()
        elif choice == "n":
            # Next room
            if enemies:
                type_out("You cannot leave the room while there are still enemies!")
            else:
                rooms_cleared += 1
                room = Room.generate_random_room()
                enemies = [generate_enemy(player.level) for _ in range(room.number_of_enemies)]
                type_out(f"You entered a new room: {room.description}")
        elif choice == "q":
            # Quit
            type_out("Thanks for playing!")
            break
        else:
            type_out("Invalid choice. Please select a valid option.")


def game_over(player, rooms_cleared):
    game_over_text = pyfiglet.figlet_format("Game Over", font="slant")
    print(game_over_text)
    type_out(f"{player.name} managed to clear {rooms_cleared} number of rooms before meeting their untimely demise.")