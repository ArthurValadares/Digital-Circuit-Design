from amaranth.lib import enum


class States(enum.Enum, shape=2):
    FORWARD = 0
    DOWN = 1
    BACK = 2
    UP = 3
