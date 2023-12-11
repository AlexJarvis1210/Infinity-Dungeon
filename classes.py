import random
from utility import type_out

class Character:
    def __init__(self, name='Player_1', health=100, strength=10, agility=10, defense=10, speed=10, spec="Rogue", XP=0, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.agility = agility
        self.defense = defense
        self.speed = speed
        self.spec = spec
        self.XP = XP
        self.level = level
        self.weapon = None
        self.assign_default_weapon()
        self.inventory = {
            "Health Potion": 2,
            "Strength Rune": 0,
            "Agility Rune": 0,
            "Defense Rune": 0,
            "Speed Rune": 0,
        }

    def __str__(self):
        return (f"Name = {self.name}\n"
                f"Health = {self.health}\n"
                f"Strength = {self.strength}\n"
                f"Agility = {self.agility}\n"
                f"Defense = {self.defense}\n"
                f"Speed = {self.speed}\n"
                f"Spec = {self.spec}\n"
                f"XP = {self.XP}\n"
                f"Level = {self.level}")

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec):
        if spec == "Rogue":
            self.health = 100
            self.strength = 50
            self.agility = 100
            self.defense = 10
            self.speed = 30

        elif spec == "Beserker":
            self.health = 150
            self.strength = 100
            self.agility = 50
            self.defense = 15
            self.speed = 20

        elif spec == "Knight":
            self.health = 200
            self.strength = 50
            self.agility = 25
            self.defense = 20
            self.speed = 10

        else:
            raise ValueError("Spec not recognised")

        self._spec = spec

    def assign_default_weapon(self):
        if self.spec == "Rogue":
            self.weapon = Weapon.venomous_dagger()
        elif self.spec == "Beserker":
            self.weapon = Weapon.orcish_warhammer()
        elif self.spec == "Knight":
            self.weapon = Weapon.rusty_iron_sword()
        else:
            raise ValueError("Spec not recognised")


    def pick_up_weapon(self, weapon):
        if self.weapon:
            type_out(f"You unequip the {self.weapon.name} and discard it.")
        self.weapon = weapon
        type_out(f"You equip the {self.weapon.name}.")


    def attack(self, enemy):
        random_modifier = random.uniform(0.9, 1.1)

        if self.weapon:
            strength_modifier = self.weapon.strength_modifier
            agility_modifier = self.weapon.agility_modifier
        else:
            strength_modifier = 1
            agility_modifier = 1

        weapon_damage = int(self.strength * strength_modifier * agility_modifier * random_modifier)
        total_damage = weapon_damage - enemy.defense
        return max(total_damage, 0)



    def damage_received(self, enemy_damage):
        damage_received = enemy_damage - self.defense
        final_damage = max(damage_received, 0)
        self.health -= final_damage
        return final_damage

    def use_health_potion(self, heal_amount=50):
        if self.inventory['Health Potion'] > 0:
            self.health = min(self.health + heal_amount, self.max_health)
            self.inventory['Health Potion'] -= 1
            type_out(f"{self.name} drinks a Health Potion and has {self.health} health.")
        else:
            type_out("You have no Health Potions!")

    def gain_xp(self, xp_amount):
        self.XP += xp_amount
        if self.level < 5:  # Level cap of 5
            self.check_level_up()

    def check_level_up(self):
        level_thresholds = [0, 100, 300, 600, 1000]

        if self.XP >= level_thresholds[self.level]:  # If XP is greater than or equal to the threshold for the next level
            self.level_up()
            type_out(str(self))

    def level_up(self):
        self.level += 1
        self.health += 20
        self.max_health += 20
        self.strength += 10
        self.agility += 10
        self.defense += 10
        self.speed += 10
        print(f"{self.name} has leveled up to level {self.level}!")

    def use_buff(self, buff_type):
        buff_type = buff_type.capitalize()  # Make sure the buff_type is capitalized
        if self.inventory[f"{buff_type} Rune"] > 0:
            if buff_type == "Strength":
                self.strength += 5
            elif buff_type == "Agility":
                self.speed += 5
            elif buff_type == "Defense":
                self.defense += 5
            elif buff_type == "Speed":
                self.speed += 5
            type_out(f"{self.name} used a {buff_type} Rune!")
            self.inventory[f"{buff_type} Rune"] -= 1
        else:
            type_out(f"You don't have any {buff_type} Runes left.")



    def open_inventory(self):
        type_out("Your inventory:")
        print("----------------")
        for index, (item, buff) in enumerate(self.inventory.items()):
            if item == "weapon":
                weapons_list = ', '.join([weapon.name for weapon in buff])
                print(f"{index + 1}. {item.capitalize()} (x[{weapons_list}])")
            else:
                print(f"{index + 1}. {item.capitalize()} (x{buff})")
        print("----------------")
        item_choice = input("Choose an item to use or press (Q) to quit: ").lower()


        if item_choice.isdigit():
            choice = int(item_choice)
            if 2 <= choice <= 5:
                self.use_buff(['Strength', 'Agility', 'Defense', 'Speed'][choice - 2])
            elif choice == 1:
                self.use_health_potion()
        elif item_choice.lower() == "q":
            return
        else:
            type_out("Invalid choice. Please try again.")






class Enemy:
    def __init__(self, name, health, strength, defense, speed, level, xp_reward):
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.level = level
        self.xp_reward = xp_reward

    def __str__(self):
        return (f"Name = {self.name}\n"
                f"Health = {self.health}\n"
                f"Strength = {self.strength}\n"
                f"Defense = {self.defense}\n"
                f"Speed = {self.speed}\n"
                f"Level = {self.level}")

    def attack(self, character):
        random_modifier = random.uniform(0.9, 1.1)
        total_damage = int(((self.strength) * random_modifier) - character.defense)
        return total_damage if total_damage > 0 else 0

    def damage_received(self, character_damage):
        damage_received = character_damage - self.defense
        final_damage = max(damage_received, 0)
        self.health -= final_damage
        return final_damage

class Weapon:
    def __init__(self, name, strength_modifier, agility_modifier):
        self.name = name
        self.strength_modifier = strength_modifier
        self.agility_modifier = agility_modifier

    def __str__(self):
        return (f"Weapon Name: {self.name}\n"
                f"Strength Modifier: {self.strength_modifier}\n"
                f"Agility Modifier: {self.agility_modifier}")

    @classmethod
    def rusty_iron_sword(cls):
        return cls("Rusty Iron Sword", 0.8, 0.9)

    @classmethod
    def wooden_staff(cls):
        return cls("Wooden Staff", 0.9, 1.1)

    @classmethod
    def elven_bow(cls):
        return cls("Elven Bow", 1.2, 1.3)

    @classmethod
    def orcish_warhammer(cls):
        return cls("Orcish Warhammer", 1.4, 0.7)

    @classmethod
    def dwarven_axe(cls):
        return cls("Dwarven Axe", 1.3, 0.8)

    @classmethod
    def enchanted_greatsword(cls):
        return cls("Enchanted Greatsword", 1.5, 1.0)

    @classmethod
    def fireball_scepter(cls):
        return cls("Fireball Scepter", 1.1, 1.4)

    @classmethod
    def venomous_dagger(cls):
        return cls("Venomous Dagger", 1.0, 1.5)

    @classmethod
    def divine_halberd(cls):
        return cls("Divine Halberd", 1.6, 1.1)

    @classmethod
    def diamond_encrusted_longsword(cls):
        return cls("Diamond Encrusted Longsword", 1.8, 1.2)

    def min_max_damage(self, character):
        min_modifier = 0.9
        max_modifier = 1.1

        strength_modifier = self.strength_modifier
        agility_modifier = self.agility_modifier

        min_damage = int(character.strength * strength_modifier * agility_modifier * min_modifier)
        max_damage = int(character.strength * strength_modifier * agility_modifier * max_modifier)

        return min_damage, max_damage


class Room:
    def __init__(self, number_of_enemies=0, treasure_chest=None, description="", weapon_drop_chance=0.3):
        self.number_of_enemies = number_of_enemies
        self.treasure_chest = treasure_chest if treasure_chest is not None else {}
        self.description = description
        self.weapon_drop_chance = weapon_drop_chance


    @staticmethod
    def generate_treasure_chest():
        items = {
            "Health Potion": random.randint(0, 3),
            "Strength Rune": random.randint(0, 1),
            "Agility Rune": random.randint(0, 1),
            "Defense Rune": random.randint(0, 1),
            "Speed Rune": random.randint(0, 1),
        }
        return {item: quantity for item, quantity in items.items() if quantity > 0}

    def generate_loot(self):
        # The new weapons list using the Weapon class
        weapons_list = [
            Weapon.rusty_iron_sword(),
            Weapon.wooden_staff(),
            Weapon.elven_bow(),
            Weapon.orcish_warhammer(),
            Weapon.dwarven_axe(),
            Weapon.enchanted_greatsword(),
            Weapon.fireball_scepter(),
            Weapon.venomous_dagger(),
            Weapon.divine_halberd(),
            Weapon.diamond_encrusted_longsword(),
        ]

        if random.random() < 0.3:  # 30% chance to drop a weapon
            weapon = random.choice(weapons_list)
            self.treasure_chest["Weapon"] = weapon


    def search_room(self, player):
        if self.number_of_enemies == 0 and self.treasure_chest:
            type_out(f"You found a treasure chest and received the following items:")
            self.generate_loot()  # Call the generate_loot method here
            for item, quantity in self.treasure_chest.items():
                if item != "Weapon":
                    type_out(f"{item}: {quantity}")
                    player.inventory[item] += quantity
                else:
                    min_damage, max_damage = quantity.min_max_damage(player)
                    type_out(f"Weapon: {quantity.name}: {min_damage} - {max_damage} damage per hit")
                    if player.weapon:
                        current_min_damage, current_max_damage = player.weapon.min_max_damage(player)
                        type_out(f"Current Weapon: {player.weapon.name}: {current_min_damage} - {current_max_damage} damage per hit")
                    swap_weapon = input("Do you want to swap your current weapon for this one? (Y)es/(N)o: ").lower()
                    if swap_weapon == 'y':
                        player.pick_up_weapon(quantity)  # Pass the Weapon object directly
            self.treasure_chest = {}  # Empty the treasure chest
        elif self.number_of_enemies == 0:
            type_out("You searched the room, but there is no treasure chest.")
        else:
            type_out("You cannot search the room while there are enemies present.")

    @classmethod
    def generate_random_room(cls):
        number_of_enemies = random.randint(1, 2)
        treasure_chest = cls.generate_treasure_chest() if random.choice([True, False]) else {}
        enemy_description = f"{number_of_enemies} {'enemy' if number_of_enemies == 1 else 'enemies'}"

        descriptions = [
            lambda: f"a mysterious room with {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a dimly lit chamber filled with eerie shadows, housing {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"an ancient, dusty hall with crumbling walls, containing {enemy_description} and {'a hidden treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a vast, echoing cavern with water dripping from the ceiling, featuring {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a claustrophobic cell with flickering torchlight, where {enemy_description} lurk and {'a treasure chest awaits' if treasure_chest else 'no treasure chest can be found'}.",
            lambda: f"a cold, stone chamber with wind whistling through the cracks, hiding {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a humid, moss-covered grotto with the smell of decay in the air, concealing {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a forgotten library filled with dusty tomes and cobwebs, inhabited by {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"a once-grand throne room, now fallen into disrepair, guarded by {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
            lambda: f"an eerily silent crypt with stone sarcophagi lining the walls, watched over by {enemy_description} and {'a treasure chest' if treasure_chest else 'no treasure chest'}.",
]

        description = random.choice(descriptions)()
        return cls(number_of_enemies, treasure_chest, description)

    def display_room_contents(self):
        print(f"Room Description: {self.description}")
        print(f"Number of Enemies: {self.number_of_enemies}")
        print(f"Treasure Chest: {'Yes' if self.treasure_chest else 'No'}")