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
@click.option("--dataset-path", "-d", required=True)
@click.option("--output-path", "-o", required=True)
@click.option(
    "--output-frame-rate",
    required=False,
    help="The frame rate of the output video. The less the faster the processing finishes.",
)
@click.option(
    "--max-frames", required=False, help="Maximum number of frames to process. This shortens the original video."
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
