from typing import Optional

import click

from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.models.detection import EfficientDetD6
from tsa.models.tracking import DeepSORT
from tsa.exporter import save_as_video


@click.group()
def cli():
    pass


@click.command(help="Run the model.")
@click.option(
    "-d", "dataset_path", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
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
    "--max-frames",
    type=int,
    required=False,
    help="Maximum number of frames to process. This shortens the original video.",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def run_model(
    dataset_path: str,
    output_path: str,
    output_frame_rate: Optional[int] = None,
    max_frames: Optional[int] = None,
    config_file: Optional[str] = None,
):
    if config_file is not None:
        config.extend_with_json(config_file)

    dataset = VideoFramesDataset(dataset_path, output_frame_rate, max_frames)
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

    save_as_video(prediction_model, tracking_model, dataset, output_path, output_frame_rate, (1280, 720))


cli.add_command(run_model)


if __name__ == "__main__":
    cli()
