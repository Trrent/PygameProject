from time import time
from pygame.sprite import Sprite, spritecollide
from pygame.surface import Surface, SurfaceType
from pygame.mask import from_surface

from Physics import Point, Vector, g
from Main import height, platforms
from typing import Union, Any


class Entity:
    def __init__(self, position: Point, velocity: float, health: float, damage: float, cooldown: float):
        """
        Базовый класс сущности
        :param position: начальная позиция; Point
        :param velocity: собственная скорость; float
        :param health: максимальное здоровье; float
        :param damage: собственный урон; float
        :param cooldown: промежуток времени между повторным ударом; float
        """
        self.pos = position
        self.vel = velocity
        self.hp = health
        self.damage = damage
        self.cooldown = cooldown

        self.last_hit = time()

    def try_hit(self, entity):
        if not issubclass(entity, Entity):
            raise Exception("Не понятно как ударить не наследника Entity")
        if self.last_hit + self.cooldown > time():
            return None
        # TODO обработка события "нанесен удар"
        self.last_hit = time()

    def take_damage(self, damage):
        pass
        # TODO обработка события "получен урон"


class GroundEntity(Entity):
    def __init__(self, position: Point, velocity: float, health: float, damage: float, cooldown: float, jump_height: float):
        """
        Базовый класс наземной сущности
        :param position: начальная позиция; Point
        :param velocity: собственная скорость; float
        :param health: максимальное здоровье; float
        :param damage: собственный урон; float
        :param cooldown: промежуток времени между повторным ударом; float
        :param jump_height: максимальная высота прыжка в пикселях; float
        """
        super().__init__(position, velocity, health, damage, cooldown)
        self.jump_h = jump_height
        self.jump_vel = (self.jump_h * 2 * g) ** 0.5
        self.jump_time = self.jump_vel / g
        self.jumped = False
        self.grounded = False
        self.mov_dir = Vector((0, 0))

        self.end_pos = self.pos
        self.jump_start = None
        self.fall_start = None

    def move_to(self, point):
        self.end_pos = Point(point[0], point[1])

    def calculate_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        if self.jumped:
            if self.jump_start is None:
                self.grounded = False
                self.jump_start = time()
            t = time() - self.jump_start
            if t < self.jump_time:
                vy = self.jump_vel - g * t
                self.mov_dir.j += vy
            else:
                self.jumped = False
                self.fall_start = time()
        if not (self.grounded or self.jumped):
            if self.fall_start is None:
                self.fall_start = time()
            t = time() - self.fall_start
            vy = -g * t
            self.mov_dir.j += vy


class Enemy(Sprite):
    pass


class ExampleEnemy(GroundEntity, Enemy):
    def __init__(self, position: Point, image: Surface | SurfaceType, velocity=10.0, health=100.0, damage=10.0, cooldown=2.0,
                 jump_height=100.0):
        super().__init__(position, velocity, health, damage, cooldown, jump_height)
        Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)

        self.last_call = None

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.last_call is None:
            dt = 0.015
        else:
            dt = time() - self.last_call
        self.calculate_mov_dir()
        dt = 1
        self.pos.x += dt * self.mov_dir.i * self.vel / (2 * self.vel) ** 0.5
        self.pos.y += dt * self.mov_dir.j * self.vel / (2 * self.vel) ** 0.5
        self.pos.upd()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
