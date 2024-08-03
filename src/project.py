from amaranth import Module, Signal, ClockDomain, Cat
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from src.pixel_gen import PixelGenerator
from src.vga_sync import VgaSync


class Project(wiring.Component):
    key: In(2)
    sw: In(10)

    vga_b: Out(4)
    vga_g: Out(4)
    vga_hs: Out(1)
    vga_r: Out(4)
    vga_vs: Out(1)

    def elaborate(self, platform):
        m = Module()

        async_resent_n = Signal(1)
        sync_resent_n = Signal(1)

        video_on = Signal(1)

        pixel_tick = Signal(1)

        right_k = Signal(1)
        left_k = Signal(1)

        pixel_x = Signal(10)
        pixel_y = Signal(10)

        rgb_reg = Signal(12)
        rgb_next = Signal(12)

        m.d.sync += sync_resent_n.eq(sync_resent_n)
        m.domains.jtag = ClockDomain(clk_edge="neg", local=True)

        m.d.jtag += right_k.eq(~self.key[0])
        m.d.sync += left_k.eq(~self.key[1])

        vga = VgaSync()
        m.submodules.vga = vga

        video_on = Signal()

        m.d.sync += [
            vga.reset_n.eq(sync_resent_n),
            self.vga_hs.eq(vga.hsync),
            pixel_tick.eq(vga.p_tick),
            pixel_x.eq(vga.pixel_x),
            pixel_y.eq(vga.pixel_y),
            video_on.eq(vga.video_on)
        ]

        pixel_gen = PixelGenerator()
        m.submodules.pixel_gen = pixel_gen

        m.d.sync += [
            pixel_gen.reset_n.eq(sync_resent_n),
            pixel_gen.video_on.eq(video_on),
            pixel_gen.p_tick.eq(pixel_tick),
            pixel_gen.right_k.eq(right_k),
            pixel_gen.left_k.eq(left_k),
            pixel_gen.pixel_x.eq(pixel_x),
            pixel_gen.pixel_y.eq(pixel_y),
            rgb_next.eq(pixel_gen.r),
            rgb_next.eq(pixel_gen.g),
            rgb_next.eq(pixel_gen.b),
        ]

        with m.If(pixel_tick):
            m.d.comb += rgb_reg.eq(rgb_next)

        m.d.comb += Cat(self.vga_r, self.vga_g, self.vga_b).eq(rgb_reg)

        return m
