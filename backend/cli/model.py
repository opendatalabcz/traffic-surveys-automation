from typing import Optional

import click

from tsa.datasets.video import VideoDataset
from tsa.enums import DetectionModelType
from tsa.models.detection import DetectionModel
from tsa.utils import save_as_video


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
def run_model(
    dataset_path: str, output_path: str, output_frame_rate: Optional[int] = None, max_frames: Optional[int] = None
):
    dataset = VideoDataset(dataset_path, output_frame_rate, max_frames)
    model = DetectionModel(DetectionModelType.faster_rcnn)

    save_as_video(model, dataset, output_path, output_frame_rate, (1280, 720))


cli.add_command(run_model)


if __name__ == "__main__":
    cli()
