from pathlib import Path
from typing import Optional

import click

from tsa import processes
from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.models.detection import EfficientDetD6
from tsa.models.tracking import DeepSORT
from tsa.storage import FileStorageMethod


@click.command(help="Run the model and store outputs in a file.")
@click.option(
    "-d", "dataset_path", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
)
@click.option(
    "-o",
    "output_file",
    type=click.Path(writable=True),
    required=True,
    help="Path where to store the output file.",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def export_to_file(
    dataset_path: str,
    output_file: Path,
    config_file: Optional[str] = None,
):
    if config_file is not None:
        config.extend_with_json(config_file)

    dataset = VideoFramesDataset(dataset_path, config.VIDEO_FRAME_RATE, config.VIDEO_MAX_FRAMES)
    prediction_model = EfficientDetD6(
        config.ED_MAX_OUTPUTS,
        config.ED_IOU_THRESHOLD,
        config.ED_SCORE_THRESHOLD,
        config.ED_NSM_SIGMA,
        config.ED_BATCH_SIZE,
    )
    tracking_model = DeepSORT(
        config.DEEP_SORT_MIN_UPDATES,
        config.DEEP_SORT_MAX_AGE,
        config.DEEP_SORT_IOU_THRESHOLD,
        config.DEEP_SORT_MAX_COSINE_DISTANCE,
        config.DEEP_SORT_MAX_MEMORY_SIZE,
    )

    tracking_generator = processes.run_detection_and_tracking(dataset, prediction_model, tracking_model)

    processes.store_tracks(tracking_generator, FileStorageMethod(output_file))


if __name__ == "__main__":
    export_to_file()
