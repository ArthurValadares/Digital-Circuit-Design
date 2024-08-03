from amaranth import Module, Cat, Signal
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from src.direction_controller import DirectionController

MAX_X = 640
MAX_Y = 480

SQUARE_SIZE = 25
SQUARE_X = 100
SQUARE_Y = 150
SQUARE_COLOR = 0x5af
SQUARE_STEP = 1


class Square(wiring.Component):
    reset_n: In(1)
    refr_tick: In(1)
    turn_right: In(1)
    turn_left: In(1)

    x: In(10)
    y: In(10)

    square_rgb: Out(12)
    square_on: Out(1)

    def elaborate(self, platform):
        m = Module()

        x_count = Signal(1)
        y_count = Signal(1)

        x_updown = Signal(1)
        x_en = Signal(1)
        y_updown = Signal(1)
        y_en = Signal(1)

        self.square_rgb = SQUARE_COLOR
        self.square_on = (x_count < self.x) & (self.x < x_count + SQUARE_SIZE) & (y_count < self.y) & (
                self.y < y_count + SQUARE_SIZE)

        # Control for x counter
        with m.If(self.reset_n == 0):
            x_count = SQUARE_X

        with m.Elif((x_en == 1).bool() & (self.refr_tick == 1).bool()):
            with m.If(x_updown == 1):
                x_count = x_count + SQUARE_STEP if (x_count < MAX_X - 1 - SQUARE_STEP) else 0

            with m.Elif(x_updown == 0):
                x_count = x_count - SQUARE_STEP if (x_count > SQUARE_STEP) else MAX_X - 1

        # Control for y counter
        with m.If(self.reset_n == 0):
            y_count = SQUARE_Y

        with m.Elif((x_en == 1).bool() & (self.refr_tick == 1).bool()):
            with m.If(x_updown == 1):
                y_count = y_count + SQUARE_STEP if (y_count < MAX_X - 1 - SQUARE_STEP) else 0

            with m.Elif(x_updown == 0):
                y_count = y_count - SQUARE_STEP if (y_count > SQUARE_STEP) else MAX_Y - 1

        m.submodules.fsm = fsm = DirectionController()

        m.d.comb += [
            fsm.reset_n.eq(self.reset_n),
            fsm.turn_right.eq(self.turn_right),
            fsm.turn_left.eq(self.turn_left),
            Cat(y_updown, y_en, x_updown, x_en).eq(fsm.data_out)
        ]

        return m
