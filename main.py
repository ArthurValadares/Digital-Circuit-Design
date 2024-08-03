from pathlib import Path

import click
from amaranth.back import verilog
from amaranth.sim import Simulator

from src.project import Project


@click.group()
def main():
    pass


@main.command()
@click.argument("OUTPUT_FILE", type=click.Path(path_type=Path, exists=False, dir_okay=False, file_okay=True))
def simulate(output_file: Path):
    dut = Project()
    sim = Simulator(dut)
    sim.run()
    sim.write_vcd(output_file)


@main.command()
@click.argument("OUTPUT_FILE", type=click.Path(exists=False, dir_okay=False, file_okay=True))
def parse(output_file: Path):
    dut = Project()
    with open(output_file, "w") as f:
        f.write(verilog.convert(dut))


if __name__ == '__main__':
    main()
