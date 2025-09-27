
import random
import time
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def hp_bar(name, icon, hp, max_hp):
    bar = "█" * hp + "-" * (max_hp - hp)
    return f"{name} {icon} [{bar}] {hp}/{max_hp}"

def animate_attack(attacker, defender):

    for frame in ["⚔️      ", "  ⚔️    ", "    ⚔️  ", "      ⚔️💥"]:
        print(f"{attacker} атакует {defender}{frame}")
        time.sleep(0.2)
        clear_screen()

def get_valid_choice(prompt, min_val, max_val):

    while True:
        choice = input(prompt)
        if choice.isdigit():
            choice = int(choice)
            if min_val <= choice <= max_val:
                return choice
        print(f"Введите число от {min_val} до {max_val}!")

def get_yes_no(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ["y", "n", "у", "н"]:
            return choice in ["y", "у"]
        print("Введите 'y' или 'n' (или 'у'/'н').")


CLASS_OF_CHARACTER = {
    'Воин': {'hp_per_level': 5, 'starting_weapon': ("Меч", 3, "Рубящий")},
    'Варвар': {'hp_per_level': 6, 'starting_weapon': ("Дубина", 3, "Дробящий")},
    'Разбойник': {'hp_per_level': 4, 'starting_weapon': ("Кинжал", 2, "Колющий")}
}

CLASS_OF_ICONS = {'Воин': '⚔️', 'Варвар': '💪', 'Разбойник': '🗡️'}
CLASS_OF_CHOSE = {1: 'Воин', 2: 'Варвар', 3: 'Разбойник'}

MONSTERS = [
    {"name": "Гоблин", "hp": 5, "weapon": ("Кинжал", 2, "Колющий"),
     "strength": 1, "dexterity": 1, "endurance": 1, "drop": ("Кинжал", 2, "Колющий")},
    {"name": "Скелет", "hp": 10, "weapon": ("Дубина", 2, "Дробящий"),
     "strength": 2, "dexterity": 2, "endurance": 1, "drop": ("Дубина", 3, "Дробящий")},
    {"name": "Слайм", "hp": 8, "weapon": ("Копье", 1, "Колющий"),
     "strength": 3, "dexterity": 1, "endurance": 2, "drop": ("Копье", 3, "Колющий")},
    {"name": "Призрак", "hp": 6, "weapon": ("Меч", 3, "Рубящий"),
     "strength": 1, "dexterity": 3, "endurance": 1, "drop": ("Меч", 3, "Рубящий")},
    {"name": "Голем", "hp": 10, "weapon": ("Топор", 1, "Рубящий"),
     "strength": 3, "dexterity": 1, "endurance": 3, "drop": ("Топор", 4, "Рубящий")},
    {"name": "Дракон", "hp": 20, "weapon": ("Легендарный Меч", 4, "Рубящий"),
     "strength": 3, "dexterity": 3, "endurance": 3, "drop": ("Легендарный Меч", 10, "Рубящий")},
]

MONSTER_ICONS = {
    "Гоблин": "👺",
    "Скелет": "💀",
    "Слайм": "🟢",
    "Призрак": "👻",
    "Голем": "🪨",
    "Дракон": "🐉"
}


class Character:
    def __init__(self, name, hp, strength, dexterity, endurance, weapon):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.weapon = weapon
        self.attack_count = 0
        self.turn_count = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage, source=None):
        self.hp = max(0, self.hp - damage)


class Hero(Character):
    def __init__(self, name, hero_class, strength, dexterity, endurance):
        self.weapon = CLASS_OF_CHARACTER[hero_class]['starting_weapon']
        self.base_hp = CLASS_OF_CHARACTER[hero_class]['hp_per_level'] + endurance
        super().__init__(name, self.base_hp, strength, dexterity, endurance, self.weapon)
        self.levels = {'Воин': 0, 'Варвар': 0, 'Разбойник': 0}
        self.levels[hero_class] = 1
        self.total_levels = 1
        self.icon = CLASS_OF_ICONS[hero_class]

    def reset_battle_state(self):
        self.turn_count = 0
        self.attack_count = 0

    def attack(self, target):
        self.attack_count += 1
        self.turn_count += 1
        animate_attack(self.name, target.name)

        if not self.hit_chance(self.dexterity, target.dexterity):
            print(f"{self.name} промахнулся!")
            return

        base = self.weapon[1] + self.strength
        bonus = 0
        desc = ""

        # Бонусы классов
        if self.levels['Разбойник'] >= 1 and self.dexterity > target.dexterity:
            bonus += 1
            desc += "Скрытая атака +1. "

        if self.levels['Разбойник'] >= 3 and self.attack_count > 1:
            bonus += (self.attack_count - 1)
            desc += f"Яд +{self.attack_count-1}. "

        if self.levels['Воин'] >= 1 and self.attack_count == 1:
            bonus += self.weapon[1]
            desc += "Порыв к действию. "

        if self.levels['Варвар'] >= 1:
            if self.attack_count <= 3:
                bonus += 2
                desc += "Ярость +2. "
            else:
                bonus -= 1
                desc += "Ярость -1. "

        damage = max(0, base + bonus)
        target.take_damage(damage, source=self)
        print(f"{self.name} наносит {damage} урона. {desc}")

    def take_damage(self, damage, source=None):
        if self.levels["Воин"] >= 2 and source and source.strength < self.strength:
            damage -= 3
        if self.levels["Варвар"] >= 2:
            damage -= self.endurance
        damage = max(0, damage)
        self.hp = max(0, self.hp - damage)
        print(f"{self.name} получает {damage} урона. HP = {self.hp}/{self.max_hp}")

    @staticmethod
    def hit_chance(attacker_dex, target_dex):
        roll = random.randint(1, attacker_dex + target_dex)
        return roll > target_dex

    def level_up(self):
        if self.total_levels == 3:
            print("Максимальный уровень.")
            return
        print("Выберите класс для прокачки:")
        for i, cls in CLASS_OF_CHOSE.items():
            print(f"{i}. {cls}")
        choice = get_valid_choice("> ", 1, 3)
        select_class = CLASS_OF_CHOSE[choice]
        self.levels[select_class] += 1
        self.total_levels += 1
        self.max_hp += CLASS_OF_CHARACTER[select_class]['hp_per_level']
        self.hp = self.max_hp
        print(f"{self.name} теперь {self.levels} уровней. HP = {self.hp}/{self.max_hp}")

class Monster(Character):
    def __init__(self, template):
        super().__init__(template["name"], template["hp"], template["strength"],
                         template["dexterity"], template["endurance"], template["weapon"])
        self.drop = template["drop"]

    def attack(self, target):
        self.attack_count += 1
        self.turn_count += 1
        animate_attack(self.name, target.name)

        if not Hero.hit_chance(self.dexterity, target.dexterity):
            print(f"{self.name} промахнулся!")
            return

        base = self.weapon[1] + self.strength
        bonus = 0
        desc = ""

        if self.name == "Слайм" and target.weapon[2] == "Рубящий":
            base = self.strength
            desc += "Слайм невосприимчив к рубящему оружию. "

        if self.name == "Скелет" and target.weapon[2] == "Дробящий":
            base *= 2
            desc += "Скелет получает двойной урон. "

        if self.name == "Дракон" and self.attack_count % 3 == 0:
            bonus += 3
            desc += "Огненное дыхание +3. "

        damage = max(0, base + bonus)
        target.take_damage(damage, source=self)
        print(f"{self.name} наносит {damage} урона. {desc}")


class Game:
    def __init__(self):
        self.hero = None
        self.victories = 0

    def menu(self):
        clear_screen()
        print("Добро пожаловать в автобатлер хорошей игры")
        print("1. Создать героя")
        print("2. Выйти")
        choice = get_valid_choice("Ваш выбор ", 1, 2)
        if choice == 1:
            self.create_hero()
            self.play()
        else:
            print("Выход из игры.")


    def create_hero(self):
        clear_screen()
        print("Выберите класс героя:")
        for i, cls in enumerate(CLASS_OF_CHARACTER.keys(), 1):
            print(f"{i}. {cls}")
        choice = get_valid_choice("Ваш выбор  ", 1, 3)
        selected_class = list(CLASS_OF_CHARACTER.keys())[choice - 1]

        strength = random.randint(1, 3)
        dexterity = random.randint(1, 3)
        endurance = random.randint(1, 3)
        name = input("Введите имя героя: ")

        self.hero = Hero(name, selected_class, strength, dexterity, endurance)
        print(f"Создан {selected_class} {name} со статами: "
              f"Сила {strength}, Ловкость {dexterity}, Выносливость {endurance}")
        self.play()

    def battle(self, monster):
        clear_screen()
        print(f"На пути встречается {monster.name} {MONSTER_ICONS.get(monster.name,'👹')}!")
        self.hero.reset_battle_state()
        monster.reset_battle_state = lambda: None

        while self.hero.is_alive() and monster.is_alive():
            print(hp_bar(self.hero.name, self.hero.icon, self.hero.hp, self.hero.max_hp))
            print(hp_bar(monster.name, MONSTER_ICONS.get(monster.name, "👹"), monster.hp, monster.max_hp))
            print()

            if self.hero.dexterity >= monster.dexterity:
                self.hero.attack(monster)
                if monster.is_alive():
                    monster.attack(self.hero)
            else:
                monster.attack(self.hero)
                if self.hero.is_alive():
                    self.hero.attack(monster)

            time.sleep(1)

        if self.hero.is_alive():
            print(f"{self.hero.name} победил {monster.name}!")
            self.victories += 1
            self.hero.hp = self.hero.max_hp
            self.after_battle(monster)
        else:
            print(f"{self.hero.name} пал в бою...")
            self.game_over()

    def after_battle(self, monster):
        if monster.drop:
            print(f"С {monster.name} выпало оружие: {monster.drop[0]} "
                  f"(урон {monster.drop[1]}, тип {monster.drop[2]})")
            if get_yes_no(f"Хотите заменить текущее оружие? (y/n): {self.hero.weapon[0]} урон {self.hero.weapon[1]} тип {self.hero.weapon[2]} "):
                self.hero.weapon = monster.drop
                print(f"{self.hero.name} теперь использует {self.hero.weapon}!")

        if self.victories < 5:
            self.hero.level_up()
        else:
            print("Поздравляем! Вы победили 5 монстров и прошли игру!")
            self.game_over()

    def play(self):
        while self.hero and self.hero.is_alive() and self.victories < 5:
            monster_template = random.choice(MONSTERS)
            monster = Monster(monster_template)
            self.battle(monster)

    def game_over(self):
        if get_yes_no("Хотите сыграть снова? (y/n): "):
            self.victories = 0
            self.create_hero()
            self.play()
        else:
            print("Спасибо за игру!")




g=Game()
g.menu()

