from pathlib import Path
from typing import List, Tuple

import click

from tsa.dataclasses.geometry.line import Line
from tsa.processes.count_vehicles import count_vehicles
from tsa.storage import FileStorageMethod


@click.command(help="Run the counting process.")
@click.option("-f", "tracks_file", type=click.Path(exists=True), required=True, help="Path with vehicle tracks.")
@click.option("-l", "lines", type=float, nargs=4, multiple=True, required=True, help="Line in format (x1, y1, x2, y2).")
def run_count_vehicles(tracks_file: Path, lines: List[Tuple[float, float, float, float]]):
    file_storage = FileStorageMethod(Path(tracks_file))

    lines = [Line(((x1, y1), (x2, y2))) for x1, y1, x2, y2 in lines]

    results = count_vehicles(file_storage, lines)

    print(results)


if __name__ == "__main__":
    run_count_vehicles()
