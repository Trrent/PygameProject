from time import time
from Physics import Vector, g
from Physics import convert_coord as cnv
from Main import height


class Entity:
    def __init__(self, pos_x: int, pos_y: int, velocity: float, damage: float, cooldown: float, health: float, weight: float):
        """
        :param pos_x: позиция по x; int
        :param pos_y: позиция по y; int
        :param velocity: собственная скорость сущности; float
        :param damage: собственный урон сущности; float
        :param cooldown: время между повторным ударом; float
        :param health: собственное здоровье сущности; float
        :param weight: собственная масса, кг; float
        """
        self.pos_x, self.pos_y = pos_x, pos_y
        self.max_vel = velocity
        self.vel = Vector(0, 0)  # instantaneous velocity
        self.weight = weight
        self.health = health
        self.damage = damage
        self.cooldown = cooldown
        self.last_hit: float = time()

    def take_damage(self, sender, damage):
        """
        Обработка события "получен урон"
        :param sender: отправитель урона; Entity subclass
        :param damage: урон; float
        :return: None
        """

    def send_damage(self, recipient):
        """
        Обработка события "нанесен урон"
        :param recipient: получатель урона; Entity subclass
        :return: None
        """


class GroundEntity(Entity):
    def __init__(self, pos_x: int, pos_y: int, velocity: float, damage: float, cooldown: float, health: float, weight: float, jump_force: Vector):
        super().__init__(pos_x, pos_y, velocity, damage, cooldown, health, weight)
        self.jump_force = jump_force
        self.mov_dir = Vector(0, 0)  # movement direction


class FlyingEntity(Entity):
    def __init__(self, pos_x: int, pos_y: int, velocity: float, damage: float, cooldown: float, health: float, weight: float):
        super().__init__(pos_x, pos_y, velocity, damage, cooldown, health, weight)

        self.mov_dir = Vector(0, 0)

    def move_to(self):
            pass
