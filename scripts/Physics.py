from math import acos
from Main import height
from collections.abc import Iterable


class Point:
    def __init__(self, x: float, pg_y: float):
        """
        Инициализация точки в классической декартовой координатной плоскости (ось ординат направлена вверх)
        :param x: абсцисса точки в плоскости pygame; float
        :param pg_y: ордината точки в плоскости pygame; float
        """
        self.x, self.y = x, height - pg_y
        self.pg_y = pg_y

    def classic(self):
        return self.x, self.y

    def pygame(self):
        return self.x, self.pg_y

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Vector:
    def __init__(self, vector_coords: Iterable[int, int] | Iterable[Point, Point]):
        """
        Представляет вектор в классической декартовой координатной плоскости.
        Если isinstance(vector_coords, Iterable), то подразумевается исходная соотнесённость с классической декартовой
        координатной плоскостью: vector{i, j}.
        Иначе расчет: i = конец.x - начало.x, j = конец.y - начало.y
        Iterable[0] = Point1 (начало)
        Iterable[1] = Point2 (конец)
        :param vector_coords:
        """
        vector_coords = list(vector_coords)
        if isinstance(vector_coords[0], int):
            self.i, self.j = vector_coords
        else:
            point1, point2 = vector_coords
            self.i = point2.x - point1.x
            self.j = point2.y - point1.y

    def get_coords(self):
        return self.i, self.j

    def __add__(self, other):
        return Vector((self.i + other.i, self.j + other.j))

    def __iadd__(self, other):
        self.i += other.i
        self.j += other.j
        return self

    def __sub__(self, other):
        return Vector((self.i - other.i, self.j - other.j))

    def __isub__(self, other):
        self.i -= other.i
        self.j -= other.j
        return self

    def __mul__(self, other):
        return Vector((self.i * other, self.j * other))

    def __rmul__(self, other):
        return Vector((self.i * other, self.j * other))

    def __str__(self):
        return f"Vector({round(self.i, 2)}, {round(self.j, 2)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __ne__(self, other):
        return self.i != other.i or self.j != other.j

    def length(self):
        return (self.i ** 2 + self.j ** 2) ** 0.5

    def is_collinear(self, other):
        return self.i / other.i == self.j / other.j

    def is_aligned(self, other):
        return Vector.is_collinear(self, other) and self.i / other.i > 0

    def is_equal(self, other):
        return self.__eq__(other)

    def scalar_product(self, other):
        return self.i * other.i + self.j * other.j

    def is_orthogonal(self, other):
        return self.scalar_product(other) == 0

    def angle(self, other):
        cos = (self.scalar_product(other)) / (self.length() * other.length())
        return acos(cos)

    def is_null_vector(self):
        return self.get_coords() == (0, 0)

    def normalize(self):
        self.i /= self.length()
        self.j /= self.length()

    def normalized(self):
        return Vector((self.i / self.length(), self.j / self.length()))


def distance(point1: Point, point2: Point):
    return point1.distance_to(point2)
