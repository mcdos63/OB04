import weakref
from abc import ABC, abstractmethod


class AutoRegisterMeta(type):
    _instances = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if instance not in cls._instances:
            # Добавляем экземпляр в WeakSet
            cls._instances.add(instance)
            # print(f"Added instance of {cls.__name__} to _instances")
        return instance

    @classmethod
    def get_instances(cls, target_cls):
        return {instance for instance in cls._instances if isinstance(instance, target_cls)}

    def __del__(self):
        self._instances.remove(self)
        print(f"Уничтожен «{self.__name__}» ...")
    # def delete_instance(self):
    #     print(f"Уничтожен «{self.__name__}» ...")
    #     self._instances.remove(self)
    #     del self


def view(cls):
    res = cls.get_instances(cls)
    print(f" Список класса «{cls.__name__}»: ".center(65, '-'))
    for person in res:
        print(vars(person))
    print(f' {len(res)} '.center(65, '-'))


class Monster(metaclass=AutoRegisterMeta):
    def __init__(self, name, health=100, damage=10):
        self.name = name
        self.health = health
        self.damage = damage

    def __del__(self):
        print(f"Уничтожен «{self.name}» (Monster)")
        # del self
        # AutoRegisterMeta.delete_instance(self)


class Fighter(metaclass=AutoRegisterMeta):
    def __init__(self, name, health=100, weapon=None):
        self.name = name
        self.health = health
        self.weapon = weapon

    def change_weapon(self, weapon):
        self.weapon = weapon

    def Fight(self, monster: Monster):
        self.weapon.attack()
        monster.health -= self.weapon.damage
        self.health -= monster.damage
        print(f'У {self.name} осталось {self.health} здоровья')
        print(f'У {monster.name} осталось {monster.health} здоровья')
        if monster.health <= 0:
            monster.__del__()  # удаляем monster
            if self.health > 0:
                bonus = self.weapon.damage * 5
                self.health += bonus
                print(f'Победил {self.name}! У него осталось {self.health} здоровья')
        if self.health <= 0:
            self.__del__()  # удаляем self

    def __del__(self):
        print(f"Уничтожен «{self.name}» (Fighter)")


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


s1 = Sword()
s1.attack()
b1 = Bow()
b1.attack()

p1 = Fighter('Джек', 100, 10)
print(p1.__class__.__name__)
m1 = Monster('Тролль', 100, 10)
p1.change_weapon(b1)
view(Fighter)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
p1.Fight(m1)
# del m1
# del m1
print(m1.__dict__)
view(Monster)
view(Fighter)
del m1
view(Monster)

input('Press Enter to exit')
