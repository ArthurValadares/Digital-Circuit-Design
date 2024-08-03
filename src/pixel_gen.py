from amaranth import Module, Signal, Cat
from amaranth.lib import wiring
from amaranth.lib.wiring import In

from src.square import Square

BACKGROUND_COLOR = 0x000


class PixelGenerator(wiring.Component):
    reset_n: In(1)

    video_on: In(1)
    p_tick: In(1)

    right_k: In(1)
    left_k: In(1)

    pixel_x: In(10)
    pixel_y: In(10)

    r: In(8)
    g: In(8)
    b: In(8)

    def elaborate(self, platform):
        m = Module()

        refr_tick = (self.pixel_y == 481) & (self.pixel_x == 0)

        square_rgb = Signal(12)
        square_on = Signal(1)

        m.submodules.square = square = Square()

        m.d.comb += [
            square.reset_n.eq(self.reset_n),
            square.refr_tick.eq(refr_tick),
            square.turn_right.eq(self.right_k),
            square.turn_left.eq(self.left_k),
            square.x.eq(self.pixel_x),
            square.y.eq(self.pixel_y),
            square.square_rgb.eq(square_rgb),
            square.square_on.eq(square_on)
        ]

        with m.If(~self.video_on):
            m.d.comb += Cat(self.r, self.g, self.b).eq(0)

        with m.Elif(square_on):
            m.d.comb += Cat(self.r, self.g, self.b).eq(square_rgb)

        with m.Else():
            m.d.comb += Cat(self.r, self.g, self.b).eq(BACKGROUND_COLOR)

        return m
