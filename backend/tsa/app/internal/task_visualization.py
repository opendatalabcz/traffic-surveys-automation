import io

import cv2
from starlette.responses import StreamingResponse

from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.processes.visualize_tracks import create_tracks_visualization
from tsa.storage.file import FileStorageMethod


def create_task_visualization(frame_path: str, task_file_path: str, minimum_path_length: float, clusters: int):
    dataset = VideoFramesDataset(str(config.SOURCE_FILES_PATH / frame_path))

    image = create_tracks_visualization(
        next(dataset.frames),
        FileStorageMethod(config.OUTPUT_FILES_PATH / task_file_path),
        minimum_path_length,
        clusters,
        False,
    )
    _, png_image = cv2.imencode(".png", image)

    return StreamingResponse(io.BytesIO(png_image.tobytes()), media_type="media/png")
