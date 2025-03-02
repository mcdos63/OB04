import weakref
from abc import ABC, abstractmethod

class AutoRegisterMeta(type):
    _instances = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if instance not in AutoRegisterMeta._instances:
            AutoRegisterMeta._instances.add(instance)
        return instance

class Registry(metaclass=AutoRegisterMeta):
    @classmethod
    def get_instances(cls, target_cls):
        return {instance for instance in AutoRegisterMeta._instances if isinstance(instance, target_cls)}
    def delete_self(self):
        print(f"Уничтожен «{self.name}» ... ({self.__class__.__name__})")
        AutoRegisterMeta._instances.discard(self)

def view(cls):
    res = Registry.get_instances(cls)
    print(f" Список класса «{cls.__name__}»: ".center(65, '-'))
    for person in res:
        print(vars(person))
    print(f' {len(res)} '.center(65, '-'))

class Monster(Registry):
    def __init__(self, name, health=100, damage=10):
        self.name = name
        self.health = health
        self.damage = damage

    # def delete_self(self):
    #     print(f"Уничтожен «{self.name}» ...")
    #     AutoRegisterMeta._instances.discard(self)

    # def __del__(self):
    #     print(f"Уничтожен «{self.name}» (Monster)")

class Persons(Registry):

    def __init__(self, name):
        self.name = name

    # def delete_self(self):
    #     print(f"Уничтожен «{self.name}» ... ({self.__class__.__name__})")
    #     AutoRegisterMeta._instances.discard(self)

    # def __del__(self):
    #     print(f"Уничтожен «{self.name}» (Fighter)")

class Fighter(Persons):
    def __init__(self, name, health=100, weapon=None):
        self.name = name
        self.health = health
        self.weapon = weapon

    def change_weapon(self, weapon):
        self.weapon = weapon
    def fight(self, monster: Monster):
        if not isinstance(monster, Monster):
            print("Ошибка: нельзя атаковать не монстра!")
            return

        if isinstance(self.weapon, Shield):
            print(f'«{self.name}» защитился от атаки {monster.name}, разошлись краями...')
        else:
            self.weapon.attack()
            monster.health -= self.weapon.damage
            self.health -= monster.damage
            print(f'У «{self.name}» осталось {self.health} здоровья')
            print(f'У {monster.name} осталось {monster.health} здоровья')

            if monster.health <= 0:
                monster.delete_self()
                if self.health > 0:
                    bonus = self.weapon.damage * 5
                    self.health += bonus
                    print(f'Победил «{self.name}»! У него осталось {self.health} здоровья')

            if self.health <= 0:
                print(f"«{self.name}» был убит монстром {monster.name}.")
                self.delete_self()

    def tamed(self, monster: Monster):
        if monster.health <= 0:
            print(f"{monster.name} уже мертв и не может быть приручен.")
            return

        monster.health += self.health // 2
        self.health += 10
        monster.damage = 1
        print(f'«{self.name}» приручил {monster.name}, пока...')
        print(f'У «{self.name}» осталось {self.health} здоровья')
        print(f'У {monster.name} осталось {monster.health} здоровья')

class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

class Sword(Weapon):
    def __init__(self, damage=10):
        self.damage = damage

    def attack(self):
        print('Атака мечом, урон:', self.damage)

class Bow(Weapon):
    def __init__(self, damage=12):
        self.damage = damage

    def attack(self):
        print('Атака луком, урон:', self.damage)

class Shield(Weapon):
    def __init__(self, damage=0):
        self.damage = damage

    def attack(self):
        if self.damage > 0:
            print('Атака щитом, урон:', self.damage)
        else:
            print('Щит используется только для защиты.')

# Создаем монстров и бойцов
goblin = Monster("Гоблин", health=50, damage=8)
dragon = Monster("Дракон", health=200, damage=20)
m1 = Monster("Монстр 1", health=100, damage=15)
m2 = Monster("Монстр 2", health=80, damage=5)

action_warrior = Fighter("Действующий воин", health=150, weapon=Sword())
action_archer = Fighter("Действующий лучник", health=100, weapon=Bow())
f1 = Fighter("Валериан", health=90, weapon=Sword())
f2 = Fighter("Вальдемар", health=100, weapon=Shield())

# Просмотр экземпляров
view(Monster)
view(Fighter)

# # Бой
action_warrior.fight(goblin)  # Атака гоблина
f1.delete_self()
# # Просмотр экземпляров после боя
view(Monster)
view(Fighter)

input("Нажмите Enter для выхода...")