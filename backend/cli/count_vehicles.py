from pathlib import Path

import click
import numpy as np

from tsa.dataclasses.geometry.line import Line
from tsa.processes.count_vehicles import count_vehicles
from tsa.storage import FileStorageMethod


@click.command(help="Run the counting process.")
def run_count_vehicles():
    file_storage = FileStorageMethod(Path("../../datasets/jackson_hole_220123.json"))

    lines = [
        Line(np.array([[1263, 613], [378, 517]])),
        Line(np.array([[804, 380], [1216, 391]])),
        Line(np.array([[356, 493], [697, 370]])),
        Line(np.array([[1232, 418], [1218, 612]])),
    ]

    results = count_vehicles(file_storage, lines)

    print(results)


if __name__ == "__main__":
    run_count_vehicles()
