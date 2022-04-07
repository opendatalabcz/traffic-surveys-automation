from pathlib import Path
from typing import Optional

import click
import cv2

from tsa import processes
from tsa.config import config
from tsa.cv2.line_draw import LineDrawer
from tsa.processes.visualize_tracks import video_or_empty_frame
from tsa.storage import FileStorageMethod

WINDOW_NAME = "Tracks visualization"


@click.command(help="Display tracks visualization.")
@click.option(
    "-f", "tracks_file", type=click.Path(exists=True, readable=True), required=True, help="Path with vehicle tracks."
)
@click.option(
    "-d", "dataset_path", type=click.Path(exists=True, readable=True), required=False, help="Path to a video dataset."
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def visualize_tracks(tracks_file: Path, dataset_path: Optional[str], config_file: Optional[str] = None):
    if config_file is not None:
        config.extend_with_json(config_file)

    frame = video_or_empty_frame(dataset_path)

    file_storage = FileStorageMethod(tracks_file)

    visualization_frame = processes.create_tracks_visualization(
        frame, file_storage, config.VISUALIZATION_MIN_PATH_LENGTH, config.VISUALIZATION_N_CLUSTERS, False
    )

    lines_drawer = LineDrawer(frame, WINDOW_NAME)

    cv2.imshow(WINDOW_NAME, visualization_frame)
    cv2.setMouseCallback(WINDOW_NAME, lines_drawer)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for x1, y1, x2, y2 in lines_drawer.lines:
        print(f"{x1} {y1} {x2} {y2}")


if __name__ == "__main__":
    visualize_tracks()
