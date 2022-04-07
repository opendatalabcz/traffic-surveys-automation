from pathlib import Path
from typing import Optional

import click

from tsa import processes
from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.storage import FileStorageMethod, VideoStorageMethod


@click.command(help="Run the model.")
@click.option(
    "-d", "dataset_path", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
)
@click.option(
    "-f", "tracks_file", type=click.Path(exists=True, readable=True), required=True, help="Path with vehicle tracks."
)
@click.option(
    "-o",
    "output_path",
    type=click.Path(writable=True),
    required=True,
    help="Path to store the output video with detections.",
)
@click.option(
    "--output-frame-rate",
    type=int,
    required=False,
    help="The frame rate of the output video. The less the faster the processing finishes.",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def export_to_video(
    dataset_path: Path,
    tracks_file: Path,
    output_path: Path,
    output_frame_rate: Optional[int] = None,
    config_file: Optional[str] = None,
):
    if config_file is not None:
        config.extend_with_json(config_file)

    video_dataset = VideoFramesDataset(dataset_path, output_frame_rate, None)
    video_statistics = video_dataset.video_statistics

    processes.export_to_video(
        video_dataset,
        FileStorageMethod(tracks_file),
        VideoStorageMethod(
            output_path, float(video_statistics.frame_rate), video_statistics.resolution, config.VIDEO_SHOW_CLASS
        ),
    )


if __name__ == "__main__":
    export_to_video()
