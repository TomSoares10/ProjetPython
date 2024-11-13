import random

class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.inventory = []
        self.xp = 0
        self.level = 1

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        if random.randint(1, 10) > 2:  # 80% chance to hit
            damage = max(0, self.attack - target.defense)
            target.take_damage(damage)
            print(f"{self.name} 🗡️ hits {target.name} for {damage} damage!")
        else:
            print(f"{self.name} 🚫 misses the attack!")

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        if item in self.inventory:
            if item == 'Potion':
                self.hp += 20
                print(f"{self.name} 🧚 uses a 🍼 Potion and restores 20 HP!")
            elif item == 'Attack Boost':
                self.attack += 5
                print(f"{self.name} 🎉 uses an Attack Boost and gains 5 attack!")
            elif item == 'Defense Boost':
                self.defense += 5
                print(f"{self.name} 🌊 uses a Defense Boost and gains 5 defense!")
            elif item == 'Double XP':
                self.xp *= 2
                print(f"{self.name} 💎 uses a Double XP potion! XP is doubled for the next fight!")
            elif item == 'Better Weapon':
                self.attack += 10
                print(f"{self.name} 🗡️ equips a Better Weapon and gains 10 attack!")
            elif item == 'Health Elixir':
                self.hp += 50
                print(f"{self.name} 💖 uses a Health Elixir and restores 50 HP!")
            elif item == 'Escape Rope':
                print(f"{self.name} 🚪 uses an Escape Rope and escapes to a safe location!")
                return 'escape'
            self.inventory.remove(item)
        else:
            print(f"{item} is not in the inventory!")

class Monster:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.hp = level * 20
        self.attack = level * 3
        self.defense = level * 2

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        if random.randint(1, 10) > 2:  # 80% chance to hit
            damage = max(0, self.attack - target.defense)
            target.take_damage(damage)
            print(f"{self.name} 🗡️ hits {target.name} for {damage} damage!")
        else:
            print(f"{self.name} 🚫 misses the attack!")

class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue

    def interact(self):
        print(f"🧔 {self.name}: {self.dialogue}")

class Game:
    def __init__(self):
        self.player = None
        self.boss_defeated = False
        self.map_size = 5
        self.map = [["empty" for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.player_position = [self.map_size // 2, self.map_size // 2]
        self.initialize_map()
        self.npcs = [
            NPC("Old Man", "Beware of the monsters that lurk in the forest."),
            NPC("Merchant", "I have some rare items for sale, but they won't be cheap."),
            NPC("Healer", "If you are hurt, I can restore your health."),
        ]

    def initialize_map(self):
        # Place some monsters, items, chests, NPCs, and doors randomly on the map
        for _ in range(5):
            self.map[random.randint(0, self.map_size - 1)][random.randint(0, self.map_size - 1)] = "monster"
        for _ in range(5):
            self.map[random.randint(0, self.map_size - 1)][random.randint(0, self.map_size - 1)] = "item"
        for _ in range(3):
            self.map[random.randint(0, self.map_size - 1)][random.randint(0, self.map_size - 1)] = "chest"
        for _ in range(2):
            self.map[random.randint(0, self.map_size - 1)][random.randint(0, self.map_size - 1)] = "npc"
        for _ in range(2):
            self.map[random.randint(0, self.map_size - 1)][random.randint(0, self.map_size - 1)] = "door"

    def main_menu(self):
        while True:
            print("\n🌎 MAIN MENU:")
            print("1. Create New Game 🌱")
            print("2. Load Saved Game 📁")
            print("3. About 📃")
            print("4. Exit 🚪")
            choice = input("> ")

            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                print("Load Saved Game feature is not available.")
            elif choice == '3':
                print("This is a retro-style RPG game made for console.")
            elif choice == '4':
                print("Exiting game.")
                break
            else:
                print("Invalid choice, please try again.")

    def start_new_game(self):
        name = input("Please enter your name: ")
        print("Choose your class:")
        print("1. Tank (High HP, Low Attack) 🛡")
        print("2. Archer (Balanced HP, High Attack) 🌹")
        print("3. Melee (High Attack, Medium HP) 🗡")
        class_choice = input("> ")
        if class_choice == '1':
            self.player = Character(name, 150, 7, 10)
            print(f"🛡 {name}, you have chosen the Tank class with high HP and strong defense.")
        elif class_choice == '2':
            self.player = Character(name, 100, 15, 5)
            print(f"🌹 {name}, you have chosen the Archer class with balanced HP and high attack.")
        elif class_choice == '3':
            self.player = Character(name, 120, 20, 3)
            print(f"🗡 {name}, you have chosen the Melee class with high attack and medium HP.")
        else:
            print("Invalid choice, defaulting to Melee class.")
            self.player = Character(name, 120, 20, 3)
        print(f"🌲 Welcome, {name}! You find yourself in a dark forest with a knife.")
        self.play()

    def play(self):
        while self.player.hp > 0 and not self.boss_defeated:
            self.display_map()
            command = input("Where do you want to go? (north, east, south, west): ").lower()
            if command in ['north', 'east', 'south', 'west']:
                self.move_player(command)
                current_tile = self.map[self.player_position[0]][self.player_position[1]]
                if current_tile == 'monster':
                    self.encounter_monster()
                elif current_tile == 'item':
                    self.find_item()
                elif current_tile == 'chest':
                    self.find_chest()
                elif current_tile == 'npc':
                    self.encounter_npc()
                elif current_tile == 'door':
                    self.enter_new_map()
                else:
                    print("You move to a new location, but nothing happens.")
                self.map[self.player_position[0]][self.player_position[1]] = 'empty'
            else:
                print("Invalid direction!")

            if self.player.hp <= 0:
                print("You have been defeated. Game over!")

    def move_player(self, direction):
        if direction == 'north' and self.player_position[0] > 0:
            self.player_position[0] -= 1
        elif direction == 'south' and self.player_position[0] < self.map_size - 1:
            self.player_position[0] += 1
        elif direction == 'east' and self.player_position[1] < self.map_size - 1:
            self.player_position[1] += 1
        elif direction == 'west' and self.player_position[1] > 0:
            self.player_position[1] -= 1
        else:
            print("You can't move in that direction!")

    def display_map(self):
        print("\n🏘️ Map:")
        for i in range(self.map_size):
            row = ""
            for j in range(self.map_size):
                if [i, j] == self.player_position:
                    row += " 👨 "
                elif self.map[i][j] == 'empty':
                    row += " . "
                elif self.map[i][j] == 'monster':
                    row += " 👹 "
                elif self.map[i][j] == 'item':
                    row += " 🎁 "
                elif self.map[i][j] == 'chest':
                    row += " 🏰 "
                elif self.map[i][j] == 'npc':
                    row += " 👩‍🌾 "
                elif self.map[i][j] == 'door':
                    row += " 🚪 "
            print(row)

    def enter_new_map(self):
        print("You found a door! 🚪 You enter a new area.")
        self.map_size += 1
        self.map = [["empty" for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.player_position = [self.map_size // 2, self.map_size // 2]
        self.initialize_map()

    def encounter_monster(self):
        monster_level = random.randint(1, self.player.level + 1)
        monster = Monster(f"Wild Monster Level {monster_level}", monster_level)
        print(f"👹 A {monster.name} appears!")
        while monster.hp > 0 and self.player.hp > 0:
            print(f"👹 {monster.name} HP: {monster.hp}")
            print(f"🛀 {self.player.name} HP: {self.player.hp}")
            action = input("What do you want to do? (🗡 attack, 🎁 use item, 🏃 run): ").lower()
            if action == 'attack':
                self.player.attack_target(monster)
                if monster.hp > 0:
                    monster.attack_target(self.player)
            elif action == 'use item':
                print(f"Available items: {', '.join(self.player.inventory)}")
                item = input("Enter the item to use: ")
                result = self.player.use_item(item)
                if result == 'escape':
                    break
            elif action == 'run':
                print(f"🏃 {self.player.name} runs away from the {monster.name}.")
                break
            else:
                print("Invalid action!")

        if monster.hp == 0:
            print(f"🎉 {monster.name} has been defeated!")
            self.player.xp += monster.level * 10
            if self.player.xp >= self.player.level * 20:
                self.player.level += 1
                self.player.hp += 20
                self.player.attack += 2
                self.player.defense += 1
                print(f"🌱 {self.player.name} leveled up to level {self.player.level}!")

    def find_item(self):
        item = random.choice(['Potion', 'Attack Boost', 'Defense Boost', 'Health Elixir', 'Escape Rope'])
        print(f"🎁 You found a {item}!")
        self.player.add_item_to_inventory(item)

    def find_chest(self):
        chest_content = random.choice(['Better Weapon', 'Potion', 'Double XP', 'Health Elixir'])
        print(f"🏰 You found a chest! Inside, you find a {chest_content}!")
        self.player.add_item_to_inventory(chest_content)

    def encounter_npc(self):
        npc = random.choice(self.npcs)
        npc.interact()
        if npc.name == "Healer":
            if input("Do you want the Healer to restore your health? (👍 yes/👎 no): ").lower() == 'yes':
                self.player.hp = 150 if isinstance(self.player, Character) and self.player.hp < 150 else self.player.hp
                print(f"💖 {self.player.name}'s health has been fully restored!")

if __name__ == "__main__":
    game = Game()
    game.main_menu()
