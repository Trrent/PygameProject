import random

import pygame
from time import time
from typing import Any
from pygame.sprite import Sprite, spritecollideany, spritecollide
from pygame.surface import Surface, SurfaceType
from pygame.mask import from_surface
from Main import load_image
from Physics import *
from spriteGroups import all_sprites, platforms, enemies


class BaseEntity:
    def __init__(self, pos: Point, hor_vel: float, damage_cd: float, health: int, damage: int):
        self.pos = pos.copy()
        self.hor_vel = hor_vel
        self.damage_cd = damage_cd
        self.hp = health
        self.damage = damage

        self.cur_vel = Vector((0, 0))


class GroundEntity(BaseEntity):
    def __init__(self, pos: Point, hor_vel: float, damage_cd: float, health: int, damage: int, jump_height: float):
        super().__init__(pos, hor_vel, damage_cd, health, damage)
        self.jumped = False
        self.grounded = False
        self.jump_start = None
        self.fall_start = None

        self.jump_v0y = (jump_height * 2 * g) ** 0.5 // 6
        self.jump_time = self.jump_v0y / g


class Skeleton(GroundEntity, Sprite):
    def __init__(self, pos: Point, player, hor_vel=5, damage_cd=3, health=70, damage=15, jump_height=100):
        GroundEntity.__init__(self, pos, hor_vel, damage_cd, health, damage, jump_height)
        Sprite.__init__(self, all_sprites, enemies)
        self.frames = {'AttackRight': (8, 1, []), 'AttackLeft': (8, 1, []), 'DeathRight': (4, 1, []),
                       'DeathLeft': (4, 1, []), 'HitRight': (4, 1, []), 'HitLeft': (4, 1, []), 'IdleRight': (4, 1, []),
                       'IdleLeft': (4, 1, []), 'WalkRight': (4, 1, []), 'WalkLeft': (4, 1, [])}
        self.cut_sheet()
        self.direction = True
        self.current_frames = self.frames['IdleLeft'][2]
        self.cur_frame = 0
        self.image = self.current_frames[self.cur_frame]
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y
        self.mask = from_surface(self.image)
        self.trigger_radius = 200
    
    def changeFrames(self, key):
        if self.frames[key][2] != self.current_frames:
            self.current_frames = self.frames[key][2]
            self.cur_frame = 0

    def updateFrame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.current_frames)
        #if self.cur_frame == 0 and self.attacking:
        #    self.attacking = False
        self.image = self.current_frames[self.cur_frame]

    def cut_sheet(self):
        for name, (columns, rows, frames) in self.frames.items():
            sheet = load_image(f"Enemies/skeleton/{name}.png")
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
    
    def move(self, direction: Vector):
        self.cur_vel.i = direction.i
        self.cur_vel.j = direction.j

    def check_grounded(self):
        collides = pygame.sprite.spritecollide(self, platforms, False)
        for collide in collides:
            if self.jumped and not self.grounded:
                if collide.rect.bottom <= self.rect.top <= collide.rect.top:  # collide.rect.bottom >= self.rect.top and
                    self.rect.top = collide.rect.bottom
                    self.jumped = False
                    self.jump_start = None
                    self.cur_vel.j = 0
            if not self.jumped and not self.grounded:
                if collide.rect.top <= self.rect.bottom:
                    self.rect.bottom = collide.rect.top
                    self.grounded = True
                    self.fall_start = None
                    self.cur_vel.j = 0

    def check_collision(self):
        collides = pygame.sprite.spritecollide(self, platforms, False)
        for collide in collides:
            if collide.rect.left >= self.rect.right and self.cur_vel.i > 0:
                self.rect.right = collide.rect.left
                self.cur_vel.i = 0
            if collide.rect.right <= self.rect.left and self.cur_vel.i < 0:
                self.rect.left = collide.rect.right
                self.cur_vel.i = 0

    def calc_fall(self):
        if not self.grounded and not self.jumped:
            if self.fall_start is None:
                self.fall_start = time()
            t = time() - self.fall_start
            self.cur_vel.j -= g * t
        if self.grounded:
            self.fall_start = None
            self.cur_vel.j = 0

    def calc_jump(self):
        if self.jumped:
            self.grounded = False
            if self.jump_start is None:
                self.jump_start = time()
                self.cur_vel.j = 0
            t = time() - self.jump_start
            if self.jump_v0y - g * t >= 0:
                self.cur_vel.j = self.jump_v0y - g * t
            else:
                self.jumped = False
                self.jump_start = None
                self.cur_vel.j = 0
    
    def jump(self):
        if self.grounded and not self.jumped:
            self.jumped = True

    def dir_to_hero(self):
        # if distance(self.pos, self.player.pos) > self.trigger_radius:
        #     return 0
        direction = Vector((self.pos, self.player.pos))
        i_moving = 0
        if direction.i > 0:
            i_moving = 1
        elif direction.i < 0:
            i_moving = -1
        else:
            if not self.rect.colliderect(self.player.rect):
                self.jump()
        if self.grounded:
            current_platform = pygame.sprite.spritecollideany(self, platforms)
            self.rect.x += i_moving * self.hor_vel
            updated = pygame.sprite.spritecollideany(self, platforms)
            self.rect.x -= i_moving * self.hor_vel
            if updated is None:
                if i_moving > 0:
                    delta = current_platform.rect.right - self.rect.right
                else:
                    delta = abs(current_platform.rect.left - self.rect.left)
                i_moving *= (self.hor_vel - delta) / self.hor_vel
                self.jump()
        self.move(Vector((i_moving, 0)))

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.cur_vel = Vector((0, 0))
        self.dir_to_hero()
        self.calc_fall()
        self.calc_jump()
        self.check_grounded()
        self.check_collision()

        self.pos.x += self.cur_vel.i * self.hor_vel
        self.pos.y += self.cur_vel.j
        self.pos.upd()

        if self.cur_vel.i > 0:
            self.direction = True
            self.changeFrames('WalkRight')
        elif self.cur_vel.i < 0:
            self.direction = False
            self.changeFrames('WalkLeft')
        if self.cur_vel.i == 0:
            self.changeFrames('IdleRight' if self.direction else 'IdleLeft')

        self.rect.x = self.pos.x
        self.rect.y = self.pos.pg_y