import random
import time
import os

CLASS_OF_CHARACTER = {'Воин': {'Здаровье за уровень':5,'starting weapon': 'Меч'},
                      'Варвар': {'Здаровье за уровень':6,'starting weapon':'Дубина'},
                      'Разбойник': {'Здаровье за уровень':4,'starting weapon':'Кинжал'}}

CLASS_OF_WEAPON = {
                 'Меч': (4, 'Рубящий'),
                 'Дубина': (3, 'Дробящий'),
                 'Кинжал': (2, 'Колющий'),
                'Топор': (4, 'Рубящий'),
                 'Копье': (3, 'Колющий'),
                 'Легендарный меч': (10, 'Рубящий')

                }

CLASS_OF_ICONS= {'Воин':'⚔️','Варвар':'💪🏿','Разбойник':'🧗🏽‍♂️'}
CLASS_OF_CHOSE= {1:'Воин',2:'Варвар',3:'Разбойник'}
MONSTERS=[
        {"name": "Гоблин",
         "hp": 5,
         "weapon": ("Кинжал", 2, "Колющий"),
         "Сила": 1, "Ловкость": 1,
         "Выносливость": 1,
         "reward": ("Кинжал", 2, "Колющий")},
        {"name": "Скелет",
         "hp": 10,
         "weapon": ("Дубина", 2, "Дробящий"),
         "Сила": 2,
         "Ловкость": 2,
         "Выносливость": 1,
         "reward": ("Дубина", 3, "Дробящий")},
        {"name": "Слайм",
         "hp": 8,
         "weapon": ("Копье", 1, "Колющий"),
         "Сила": 3,
         "Ловкость": 1,
         "Выносливость": 2,
         "reward": ("Копье", 3, "Колющий")},
        {"name": "Призрак",
         "hp": 6,
         "weapon": ("Меч", 3, "Рубящий"),
         "Сила": 1,
         "Ловкость": 3,
         "Выносливость": 1,
         "reward": ("Меч", 3, "Рубящий")},
        {"name": "Голем",
         "hp": 10, "weapon": ("Топор", 1, "Рубящий"),
         "Сила": 3, "Ловкость": 1,
         "Выносливость": 3,
         "reward": ("Топор", 4, "Рубящий")},
        {"name": "Дракон",
         "hp": 20,
         "weapon": ("Легендарный Меч", 4, "Рубящий"),
         "Сила": 3, "Ловкость": 3,
         "Выносливость": 3,
         "reward": ("Легендарный Меч", 10, "Рубящий")},
]



class Character:

    def __init__(self,name,hp,strength,dexterity,endurance,weapon):
        self.name=name
        self.max_hp=hp
        self.hp=hp
        self.strength=strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.weapon = weapon
        self.count=0
    def is_life(self):
        if self.hp>0:
            return True

    def attack(self,target):
        damage=self.weapon[1]+self.strength
        target.hp-=damage
        print(f'{self.name} наносит {target.name} урон (НР {target.hp}/{target.max_hp}')

    def take_damage(self,damage):
        self.hp=max(0,self.hp-damage)

    def hit_chance(self,attacker_dex,target_dex):
        roll=random.randint(1,attacker_dex+target_dex)
        return roll>target_dex



class Hero(Character):
    def __init__(self,name,hero_class,strength,dexterity,endurance):

        weapon = CLASS_OF_CHARACTER[hero_class['starting weapon']]
        base_hp = CLASS_OF_CHARACTER[hero_class['Здаровье за уровень']] + endurance

        super().__init__(self, name, base_hp, strength, dexterity, endurance, weapon)

        self.levels={'Воин':0,'Варвар': 0,'Разбойник': 0}
        self.levels[hero_class]=1
        self.total_levels=1
        self.icon=CLASS_OF_ICONS[hero_class]
        self.attack_count=0


    def count_battle_state(self):
        self.turn_count=0
        self.attack_count=0

    def level_up(self):
        if self.total_levels==3:
            print('Максимальный уровень.')
            return
        print(f'Выбери класс для продвижения ')
        for i,cls  in enumerate(CLASS_OF_CHOSE.items()):
            print(f'i','cls')

        chose=self.valid_choise(input('Ваш выбор 1, 2, или 3 '))
        select_class=CLASS_OF_CHOSE[chose]
        self.levels[select_class]+=1
        self.total_levels+=1
        if select_class=='Воин':
            self.max_hp+=5
            if self.levels['Воин'] == 3:
                self.strength+=1
        if select_class=='Варвар':
            self.max_hp+=6
            if self.levels['Варвар'] == 3:
                self.endurance+=1

        if select_class=='Разбойник':
            self.max_hp+=4
            if self.levels['Разбойник'] == 2:
                self.dexterity+=1

        self.hp=self.max_hp
        print(f'{self.name} теперь {self.levels} уровней. HP итоговое  {self.max_hp}❤️')







    @staticmethod
    def valid_choise(number):
        while True:
            try:
                number = int(number)
                if 1<=number<=3:
                    return number
                else:
                    number = input('Введите значение 1, 2 или 3 ')

            except ValueError:
                number = input('Введите значение 1, 2 или 3 ')
        return number

    def hit_change(self, attacked_dex, target_dex):
        roll = random.randint(1, attacked_dex + target_dex)
        return roll > target_dex

    def new_atask_damage(self, target):
        self.attack_count += 1
        self.turn_count += 1
        if not self.hit_chance(self.dexterity, target.dexterity):
            return (False, 0, 'Промах')

        base=self.weapon[1]+self.strength
        bonus=0
        desc='Not effect'

        if self.levels['Разбойник']>=1 and self.dexterity>target.dexterity:
            bonus+=1
            desc+='Скрытая атака +1'

        if self.levels['Разбойник'] >= 3 and self.attack_count>1:

            bonus += 1
            desc += f'Яд + {bonus}'

        if self.levels['Воин'] >= 1 and self.attack_count == 1:
            bonus += self.weapon[1]
            desc += f'Порыв к действию'

        if self.levels['Варвар'] >= 1:
            if  self.attack_count <=3:
                bonus+=2
                desc+='Ярость+2'
            else:
                bonus-=1
                desc+='Ярость-1'
        damage=base+bonus
        return (True,damage,desc.strip())

    def attack(self,target):
        self.attack_count+=1
        self.turn_count+=1

        hit,damage,desc=self.new_atask_damage(target)
        if not hit:
            print(f'{self.name} промахнулся' )
            return
        else:
            target.take_damage(damage,source=self)


    def take_damage(self,damage,source=None):
        if self.levels["Воин"] >= 2 and source and source.strenght < self.strength:
            damage-=3


        if self.levels["Варвар"] >= 2:
            damage-=self.endurance
        damage=max(0,damage)
        print(f'{self.name} получает {damage} урона. HP = {self.hp}/{self.max_hp}')

    def det_main_class(self):
        for cls , lvl in self.levels.items():
            max_lvl=0
            if lvl>max_lvl:
                max_lvl=lvl
                return max_lvl
        return 'Воин'









class Game:
    def __init__(self,hero,monster):
        self.hero=hero
        self.monster=monster


    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def animate_attack(self,hero_lines,monster_lines,weapon_symbol):
        for i in range(3):
            self.clear_screen()
            for h_line,m_line in zip(hero_lines,monster_lines):
                print(f'{h_line} {weapon_symbol*i} {m_line}')
            time.sleep(0.25)


    def valid_choise(number):
        while True:
            try:
                number = int(number)
                if 1<=number<=3:
                    return number
                else:
                    number = input('Введите значение 1, 2 или 3 ')

            except ValueError:
                number = input('Введите значение 1, 2 или 3 ')

        return number


    def create_character(self,):
        print('Выбери персонажа  (Воин : 1, Варвар : 2, Разбойник : 3) ')
        choice_user=self.valid_choise(input('Введите значение 1, 2 или 3 '))
        return choice_user



    stats={
        'Сила':random.randint(1,3),
        'Ловкость':random.randint(1,3),
        'Выносливость':random.randint(1,3)
    }

print(create_character())