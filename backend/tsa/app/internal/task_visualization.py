import io
from typing import Optional

import cv2
from starlette.responses import StreamingResponse

from tsa.config import config
from tsa.processes.visualize_tracks import (create_tracks_visualization,
                                            video_or_empty_frame)
from tsa.storage.file import FileStorageMethod


def create_task_visualization(
    task_file_path: str, frame_path: Optional[str], minimum_path_length: float, clusters: int
):
    frame = video_or_empty_frame(config.SOURCE_FILES_PATH / frame_path)

    image = create_tracks_visualization(
        frame,
        FileStorageMethod(config.OUTPUT_FILES_PATH / task_file_path),
        minimum_path_length,
        clusters,
        False,
    )
    _, png_image = cv2.imencode(".png", image)

    return StreamingResponse(io.BytesIO(png_image.tobytes()), media_type="media/png")
