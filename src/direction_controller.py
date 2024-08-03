from amaranth import Module
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from src.states import States


class DirectionController(wiring.Component):
    reset_n: In(1)
    turn_right: In(1)
    turn_left: In(1)

    data_out: Out(4)

    def elaborate(self, platform):
        m = Module()

        with m.FSM(init=States.FORWARD):
            with m.State(States.FORWARD):
                m.d.sync += self.data_out.eq(0b0011)
                with m.If(self.turn_right):
                    m.next = States.DOWN

                with m.Elif(self.turn_left):
                    m.next = States.UP

            with m.State(States.DOWN):
                m.d.sync += self.data_out.eq(0b1100)
                with m.If(self.turn_right):
                    m.next = States.BACK

                with m.Elif(self.turn_left):
                    m.next = States.FORWARD

            with m.State(States.BACK):
                m.d.sync += self.data_out.eq(0b0001)
                with m.If(self.turn_right):
                    m.next = States.UP

                with m.Elif(self.turn_left):
                    m.next = States.DOWN

            with m.State(States.UP):
                m.d.sync += self.data_out.eq(0b0100)
                with m.If(self.turn_right):
                    m.next = States.FORWARD

                with m.Elif(self.turn_left):
                    m.next = States.BACK

        return m
