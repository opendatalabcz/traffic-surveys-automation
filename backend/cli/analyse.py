import asyncio
from pathlib import Path
from typing import Optional, Tuple

import click

from tsa import enums, processes
from tsa.app.celery_tasks.common import change_db_statuses
from tsa.config import config
from tsa.dataclasses.frames import VideoFramesDataset
from tsa.models import init_detection_model, init_tracking_model
from tsa.monitoring import neptune_monitor
from tsa.storage import FileStorageMethod


@click.command(help="Run the model and store outputs in a file.")
@click.option(
    "-f", "dataset_file", type=click.Path(exists=True, readable=True), required=True, help="Path to a video dataset."
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
@click.option("-i", "identifiers", nargs=2, type=int, required=False)
@click.option(
    "-c",
    "--config-file",
    type=click.Path(exists=True),
    required=False,
    help="Override the default configuration defined in tsa.config.*.config.json files.",
)
def run_analysis(
    dataset_file: Path,
    output_file: Path,
    detection_model_name: enums.DetectionModels,
    tracking_model_name: enums.TrackingModel,
    identifiers: Optional[Tuple[int, int]] = None,
    config_file: Optional[str] = None,
):
    if config_file is not None:
        config.extend_with_json(config_file)

    try:
        _change_db_statuses(identifiers, enums.SourceFileStatus.processing, enums.TaskStatus.processing)
        _run_analysis(dataset_file, output_file, detection_model_name, tracking_model_name)
    except Exception as exc:
        _change_db_statuses(identifiers, enums.SourceFileStatus.processed, enums.TaskStatus.failed)
        raise exc
    else:
        _change_db_statuses(identifiers, enums.SourceFileStatus.processed, enums.TaskStatus.completed)


def _run_analysis(
    dataset_path: Path,
    output_file: Path,
    detection_model_name: enums.DetectionModels,
    tracking_model_name: enums.TrackingModel,
):
    with neptune_monitor(
        "tsa-analysis", [detection_model_name.name, tracking_model_name.name, dataset_path.name, output_file.name]
    ):
        dataset = VideoFramesDataset(dataset_path, config.VIDEO_FRAME_RATE, config.VIDEO_MAX_FRAMES)

        prediction_model = init_detection_model(detection_model_name)
        tracking_model = init_tracking_model(tracking_model_name)

        tracking_generator = processes.run_detection_and_tracking(dataset, prediction_model, tracking_model)

        processes.store_tracks(tracking_generator, FileStorageMethod(output_file))


def _change_db_statuses(
    identifiers: Optional[Tuple[int, int]], source_file_status: enums.SourceFileStatus, task_status: enums.TaskStatus
):
    if not identifiers:
        return

    asyncio.run(change_db_statuses(identifiers[0], identifiers[1], source_file_status, task_status))


if __name__ == "__main__":
    run_analysis()
