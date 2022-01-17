import pygame
from time import time
from typing import Any
from pygame.sprite import Sprite, spritecollideany, spritecollide
from pygame.surface import Surface, SurfaceType
from pygame.mask import from_surface
from Main import load_image
from Physics import *
from spriteGroups import all_sprites, platforms, enemies


class Entity:
    def __init__(self, pos: Point, hor_vel: float, health: int, damage: int, cooldown: float):
        self.pos = pos.copy()
        self.hor_vel = hor_vel
        self.hp = health
        self.damage = damage
        self.cooldown = cooldown

        self.mov_dir = Vector((0, 0))
        self.end_pos = self.pos.copy()
    
    def changeFrames(self, key):
        self.current_frames = self.frames[key][2]

    def updateFrame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.current_frames)
        self.image = self.current_frames[self.cur_frame]


class GroundEntity(Entity):
    def __init__(self, pos: Point, hor_vel: float, health: int, damage: int, cooldown: float, jump_height: float):
        super().__init__(pos, hor_vel, health, damage, cooldown)

        self.jump_h = jump_height  # максимальная высота подъема
        self.jump_v0y = (self.jump_h * 2 * g) ** 0.5 // 6  # начальная скорость v0 = sqrt(hмакс * 2g)
        self.jump_t = self.jump_v0y / g  # tподъем = v0 / g
        self.jump_start = None
        self.jumped = False

        self.fall_start = None
        self.grounded = False

    def move(self, direction: Vector, immediately=False):
        self.end_pos = self.pos.copy()
        self.end_pos.x += direction.i
        self.end_pos.y += direction.j
        self.end_pos.upd()
        if immediately:
            self.pos = self.end_pos.copy()

    def move_to(self, pos: Point | tuple, immediately=False):
        self.end_pos = pos.copy() if type(pos) == pos else Point(pos[0], pos[1])
        if immediately:
            self.pos = self.end_pos.copy()
    
    def stop(self):
        self.end_pos.x = self.rect.x
        self.mov_dir.i = 0


class FlyingEntity(Entity):
    def __init__(self, pos: Point, hor_vel: float, ver_vel: float, health: int, damage: int, cooldown: float):
        super().__init__(pos, hor_vel, health, damage, cooldown)
        self.ver_vel = ver_vel

    def move(self, direction: Vector, immediately=False):
        self.end_pos = self.pos.copy()
        self.end_pos.x += direction.i
        self.end_pos.y += direction.j
        self.end_pos.upd()
        if immediately:
            self.pos = self.end_pos.copy()

    def move_to(self, pos: Point | tuple, immediately=False):
        self.end_pos = pos.copy() if type(pos) == pos else Point(pos[0], pos[1])
        if immediately:
            self.pos = self.end_pos.copy()


class Friend(Sprite):
    pass


class Enemy(Sprite):
    pass


class Player(GroundEntity, Friend):
    def __init__(self, pos: Point, hor_vel=10, health=100, damage=20, cooldown=1,
                 jump_height=70):
        super().__init__(pos, hor_vel, health, damage, cooldown, jump_height)
        Friend.__init__(self, all_sprites)
        self.frames = {'Attack1Right': (4, 1, []), 'DeathRight': (9, 1, []), 'FallRight': (6, 1, []),  'FallLeft': (6, 1, []),
                       'HitRight': (3, 1, []), 'IdleRight': (6, 1, []), 'IdleLeft': (6, 1, []),
                       'JumpRight': (6, 1, []),  'JumpLeft': (6, 1, []), 'RunRight': (8, 1, []), 'RunLeft': (8, 1, [])}
        self.cut_sheet()
        self.direction = True
        self.current_frames = self.frames['FallRight'][2]
        self.cur_frame = 0
        self.image = self.current_frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)
    
    def cut_sheet(self):
        for name, (columns, rows, frames) in self.frames.items():
            sheet = load_image(f"Hero/{name}.png")
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
    
    def attack(self):
        self.changeFrames('Attack1Right')
        self.updateFrame()
        for sprite in spritecollide(self, enemies, False):
            sprite.health -= self.damage

    def check_collides(self):
        self.rect.y += 1
        collides = spritecollideany(self, platforms)
        self.rect.y -= 1
        self.grounded = True if collides else False

    def calc_jump(self):
        if self.jump_start is None:
            self.grounded = False
            self.jump_start = time()
        t = time() - self.jump_start
        if t > self.jump_t:
            self.changeFrames('IdleRight' if self.direction else 'IdleLeft')
            self.jumped = False
            self.jump_start = None
            return 0
        self.changeFrames('JumpRight' if self.direction else 'JumpLeft')
        return self.jump_v0y - g * t

    def calc_fall(self):
        if self.fall_start is None:
            self.fall_start = time()
        t = time() - self.fall_start
        return -g * t

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        self.check_collides()
        vy = 0
        if self.jumped:
            vy = self.calc_jump()

        if not self.jumped and not self.grounded:
            vy = self.calc_fall()

        if self.grounded:
            if self.fall_start:
                self.changeFrames('IdleRight' if self.direction else 'IdleLeft')
            self.mov_dir.j = 0
            self.fall_start = None

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.j += vy

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.x = self.rect.x
        self.pos.pg_y = self.rect.y
        self.pos.upd()

        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (2 * self.hor_vel ** 2)
        if self.mov_dir.i > 0:
            self.direction = True
            self.changeFrames('RunRight')
        elif self.mov_dir.i < 0:
            self.direction = False
            self.changeFrames('RunLeft')
        self.pos.y += self.mov_dir.j * self.hor_vel / (2 * self.hor_vel ** 2)
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y


class Skeleton(GroundEntity, Enemy):
    def __init__(self, pos: Point, image: Surface | SurfaceType, player: Player, hor_vel=3, health=100, damage=20, cooldown=1,
                 jump_height=70):
        super().__init__(pos, hor_vel, health, damage, cooldown, jump_height)
        Enemy.__init__(self, all_sprites, enemies)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)

    def correct_trajectory(self):
        if distance(self.pos, self.player.pos) <= 10:
            self.end_pos = self.player.pos.copy()

    def check_collides(self):
        self.rect.y += 1
        collides = spritecollideany(self, platforms)
        self.rect.y -= 1
        self.grounded = False if collides is None else True

    def calc_jump(self):
        if self.jump_start is None:
            self.grounded = False
            self.jump_start = time()
        t = time() - self.jump_start
        if t > self.jump_t:
            self.jumped = False
            self.jump_start = None
            return 0
        return self.jump_v0y - g * t

    def calc_fall(self):
        if self.fall_start is None:
            self.fall_start = time()
        t = time() - self.fall_start
        return -g * t

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        self.check_collides()
        vy = 0
        if self.jumped:
            vy = self.calc_jump()

        if not self.jumped and not self.grounded:
            vy = self.calc_fall()

        if self.grounded:
            self.mov_dir.j = 0
            self.fall_start = None

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.j += vy

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.x = self.rect.x
        self.pos.pg_y = self.rect.y
        self.pos.upd()

        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.y += self.mov_dir.j * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y


class Bat(FlyingEntity, Enemy):
    def __init__(self, pos: Point, image: Surface | SurfaceType, player: Player, hor_vel=3, ver_vel=4, health=30, damage=10, cooldown=1):
        super().__init__(pos, hor_vel, ver_vel, health, damage, cooldown)
        Enemy.__init__(self, all_sprites, enemies)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos))

        if 0 < abs(self.pos.y - self.end_pos.y) <= 1.1:
            self.mov_dir.j = 0

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.normalize()

    def correct_trajectory(self):
        if distance(self.pos, self.player.pos) <= 10:
            self.end_pos = self.player.pos.copy()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.correct_trajectory()
        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (self.hor_vel ** 2 + self.ver_vel ** 2) ** 0.5
        self.pos.y += self.mov_dir.j * self.ver_vel / (self.hor_vel ** 2 + self.ver_vel ** 2) ** 0.5
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y


class FireSpirit(GroundEntity, Enemy):
    def __init__(self, pos: Point, image: Surface | SurfaceType, player: Player, hor_vel=5, health=40, damage=30, cooldown=1,
                 jump_height=50):
        super().__init__(pos, hor_vel, health, damage, cooldown, jump_height)
        Enemy.__init__(self, all_sprites, enemies)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)

    def correct_trajectory(self):
        if distance(self.pos, self.player.pos) <= 10:
            self.end_pos = self.player.pos.copy()

    def check_collides(self):
        self.rect.y += 1
        collides = spritecollideany(self, platforms)
        self.rect.y -= 1
        self.grounded = False if collides is None else True

    def calc_jump(self):
        if self.jump_start is None:
            self.grounded = False
            self.jump_start = time()
        t = time() - self.jump_start
        if t > self.jump_t:
            self.jumped = False
            self.jump_start = None
            return 0
        return self.jump_v0y - g * t

    def calc_fall(self):
        if self.fall_start is None:
            self.fall_start = time()
        t = time() - self.fall_start
        return -g * t

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        self.check_collides()
        vy = 0
        if self.jumped:
            vy = self.calc_jump()

        if not self.jumped and not self.grounded:
            vy = self.calc_fall()

        if self.grounded:
            self.mov_dir.j = 0
            self.fall_start = None

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.j += vy

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.x = self.rect.x
        self.pos.pg_y = self.rect.y
        self.pos.upd()

        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.y += self.mov_dir.j * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y


class Slime(GroundEntity, Enemy):
    def __init__(self, pos: Point, image: Surface | SurfaceType, player: Player, hor_vel=1.5, health=40, damage=30, cooldown=1,
                 jump_height=50):
        super().__init__(pos, hor_vel, health, damage, cooldown, jump_height)
        Enemy.__init__(self, all_sprites, enemies)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)

    def correct_trajectory(self):
        if distance(self.pos, self.player.pos) <= 10:
            self.end_pos = self.player.pos.copy()

    def check_collides(self):
        self.rect.y += 1
        collides = spritecollideany(self, platforms)
        self.rect.y -= 1
        self.grounded = False if collides is None else True

    def calc_jump(self):
        if self.jump_start is None:
            self.grounded = False
            self.jump_start = time()
        t = time() - self.jump_start
        if t > self.jump_t:
            self.jumped = False
            self.jump_start = None
            return 0
        return self.jump_v0y - g * t

    def calc_fall(self):
        if self.fall_start is None:
            self.fall_start = time()
        t = time() - self.fall_start
        return -g * t

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        self.check_collides()
        vy = 0
        if self.jumped:
            vy = self.calc_jump()

        if not self.jumped and not self.grounded:
            vy = self.calc_fall()

        if self.grounded:
            self.mov_dir.j = 0
            self.fall_start = None

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.j += vy

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.x = self.rect.x
        self.pos.pg_y = self.rect.y
        self.pos.upd()

        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.y += self.mov_dir.j * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y


class Wizard(GroundEntity, Enemy):
    def __init__(self, pos: Point, image: Surface | SurfaceType, player: Player, hor_vel=4, health=300, damage=35, cooldown=3,
                 jump_height=90):
        super().__init__(pos, hor_vel, health, damage, cooldown, jump_height)
        Enemy.__init__(self, all_sprites, enemies)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)

    def correct_trajectory(self):
        if distance(self.pos, self.player.pos) <= 10:
            self.end_pos = self.player.pos.copy()

    def check_collides(self):
        self.rect.y += 1
        collides = spritecollideany(self, platforms)
        self.rect.y -= 1
        self.grounded = False if collides is None else True

    def calc_jump(self):
        if self.jump_start is None:
            self.grounded = False
            self.jump_start = time()
        t = time() - self.jump_start
        if t > self.jump_t:
            self.jumped = False
            self.jump_start = None
            return 0
        return self.jump_v0y - g * t

    def calc_fall(self):
        if self.fall_start is None:
            self.fall_start = time()
        t = time() - self.fall_start
        return -g * t

    def calc_mov_dir(self):
        self.mov_dir = Vector((self.pos, self.end_pos)).normalized()
        self.check_collides()
        vy = 0
        if self.jumped:
            vy = self.calc_jump()

        if not self.jumped and not self.grounded:
            vy = self.calc_fall()

        if self.grounded:
            self.mov_dir.j = 0
            self.fall_start = None

        collides = spritecollide(self, platforms, False)
        for collide in collides:
            if self.mov_dir.i > 0:
                self.rect.right = collide.rect.left
            if self.mov_dir.i < 0:
                self.rect.left = collide.rect.right
            self.mov_dir.i = 0
        self.mov_dir.j += vy

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.x = self.rect.x
        self.pos.pg_y = self.rect.y
        self.pos.upd()

        self.calc_mov_dir()
        self.pos.x += self.mov_dir.i * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.y += self.mov_dir.j * self.hor_vel / (2 * self.hor_vel ** 2) ** 0.5
        self.pos.upd()

        if 0 < distance(self.pos, self.end_pos) <= 1.1:
            self.pos = self.end_pos.copy()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
