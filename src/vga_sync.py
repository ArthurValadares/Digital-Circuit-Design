from amaranth import Module, Signal
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

# Parâmetros da VGA
HD = 640
HF = 48
HB = 16
HR = 96
VD = 480
VF = 10
VB = 33
VR = 2


class VgaSync(wiring.Component):
    reset_n: In(1)
    hsync: Out(1)
    vsync: Out(1)
    p_tick: Out(1)
    video_on: Out(1)
    pixel_x: Out(10)
    pixel_y: Out(10)

    def elaborate(self, platform):
        m = Module()

        # Registradores e sinais
        mod2_reg = Signal(1)
        v_count_reg = Signal(10)
        h_count_reg = Signal(10)
        v_sync_reg = Signal(1)
        h_sync_reg = Signal(1)

        mod2_next = Signal(1)
        v_count_next = Signal(10)
        h_count_next = Signal(10)
        v_sync_next = Signal(1)
        h_sync_next = Signal(1)

        pixel_tick = Signal(1)
        h_end = Signal(1)
        v_end = Signal(1)

        # Bloco de registro
        with m.If(~self.reset_n):
            m.d.sync += [
                mod2_reg.eq(0),
                v_count_reg.eq(0),
                h_count_reg.eq(0),
                v_sync_reg.eq(0),
                h_sync_reg.eq(0)
            ]
        with m.Else():
            m.d.sync += [
                mod2_reg.eq(mod2_next),
                v_count_reg.eq(v_count_next),
                h_count_reg.eq(h_count_next),
                v_sync_reg.eq(v_sync_next),
                h_sync_reg.eq(h_sync_next)
            ]

        # Lógica combinacional
        m.d.comb += [
            mod2_next.eq(~mod2_reg),
            pixel_tick.eq(mod2_reg),
            h_end.eq(h_count_reg == (HD + HF + HB + HR - 1)),
            v_end.eq(v_count_reg == (VD + VF + VB + VR - 1)),
            h_sync_next.eq(((HD + HB) <= h_count_reg) & (h_count_reg <= (HD + HB + HR - 1))),
            v_sync_next.eq(((VD + VB) <= v_count_reg) & (v_count_reg <= (VD + VB + VR - 1))),
            self.video_on.eq((h_count_reg < HD) & (v_count_reg < VD)),
            self.hsync.eq(h_sync_reg),
            self.vsync.eq(v_sync_reg),
            self.pixel_x.eq(h_count_reg),
            self.pixel_y.eq(v_count_reg),
            self.p_tick.eq(pixel_tick)
        ]

        # Lógica de próxima contagem
        with m.If(pixel_tick):
            with m.If(h_end):
                m.d.comb += h_count_next.eq(0)
            with m.Else():
                m.d.comb += h_count_next.eq(h_count_reg + 1)
        with m.Else():
            m.d.comb += h_count_next.eq(h_count_reg)

        with m.If(pixel_tick & h_end):
            with m.If(v_end):
                m.d.comb += v_count_next.eq(0)
            with m.Else():
                m.d.comb += v_count_next.eq(v_count_reg + 1)
        with m.Else():
            m.d.comb += v_count_next.eq(v_count_reg)

        return m
