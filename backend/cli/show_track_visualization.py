from pathlib import Path

import click
import cv2

from tsa import processes
from tsa.datasets import VideoFramesDataset
from tsa.storage import FileStorageMethod


@click.command(help="Display tracks visualization.")
@click.option(
    "-d", "dataset_path", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
)
@click.option(
    "-f",
    "tracks_file",
    type=click.Path(writable=True),
    required=True,
    help="Path where to store the output file.",
)
def export_to_file(dataset_path: str, tracks_file: Path):
    dataset = VideoFramesDataset(dataset_path)
    frame = next(dataset.frames)

    file_storage = FileStorageMethod(tracks_file)

    visualization_frame = processes.create_tracks_visualization(frame, file_storage, 150.0, 9, False)

    cv2.imshow("Cross-road visualization", visualization_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    export_to_file()
