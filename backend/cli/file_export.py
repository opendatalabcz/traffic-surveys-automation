from pathlib import Path
from typing import Optional

import click

from tsa import enums, processes
from tsa.config import config
from tsa.dataclasses.frames import VideoFramesDataset
from tsa.models import init_detection_model, init_tracking_model
from tsa.storage import FileStorageMethod


@click.command(help="Run the model and store outputs in a file.")
@click.option(
    "-p", "dataset_path", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
)
@click.option(
    "-o",
    "output_file",
    type=click.Path(writable=True),
    required=True,
    help="Path where to store the output file.",
)
@click.option("-d", "detection_model_name", type=click.Choice(enums.DetectionModels), required=True)
@click.option("-t", "tracking_model_name", type=click.Choice(enums.TrackingModel), required=True)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def export_to_file(
    dataset_path: Path,
    output_file: Path,
    detection_model_name: enums.DetectionModels,
    tracking_model_name: enums.TrackingModel,
    config_file: Optional[str] = None,
):
    if config_file is not None:
        config.extend_with_json(config_file)

    dataset = VideoFramesDataset(dataset_path, config.VIDEO_FRAME_RATE, config.VIDEO_MAX_FRAMES)

    prediction_model = init_detection_model(detection_model_name)
    tracking_model = init_tracking_model(tracking_model_name)

    tracking_generator = processes.run_detection_and_tracking(dataset, prediction_model, tracking_model)

    processes.store_tracks(tracking_generator, FileStorageMethod(output_file))


if __name__ == "__main__":
    export_to_file()
