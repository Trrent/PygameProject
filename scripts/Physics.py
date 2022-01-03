from math import acos
from Main import height
from typing import Union


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __str__(self):
        return f"Vector({round(self.x, 2)}, {round(self.y, 2)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def is_collinear(self, other):
        return self.x / other.x == self.y / other.y

    def is_aligned(self, other):
        return Vector.is_collinear(self, other) and self.x / other.x > 0

    def is_equal(self, other):
        return self.__eq__(other)

    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y

    def is_orthogonal(self, other):
        return self.scalar_product(other) == 0

    def angle(self, other):
        cos = (self.scalar_product(other)) / (self.length() * other.length())
        return acos(cos)

    def is_null_vector(self):
        return self.get_coords() == (0, 0)

    def normalize(self):
        self.x /= self.length()
        self.y /= self.length()

    def normalized(self):
        return Vector(self.x / self.length(), self.y / self.length())


def convert_coord(point: Union[int, Vector]):
    """Конвертация координаты из одной плоскости в другую"""
    return height - point if type(point) == int else Vector(point.x, height - point.y)
