from fastapi.responses import StreamingResponse

from tsa import processes
from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.storage import FileStorageMethod, VideoStorageMethod


def create_video(source_video_path: str, analysis_path: str, output_frame_rate: int, show_classes: bool):
    video_dataset = VideoFramesDataset(config.SOURCE_FILES_PATH / source_video_path, output_frame_rate, None)
    video_statistics = video_dataset.video_statistics

    processes.export_to_video(
        video_dataset,
        FileStorageMethod(config.OUTPUT_FILES_PATH / analysis_path),
        VideoStorageMethod(
            config.OUTPUT_FILES_PATH / "tmp.mp4", float(output_frame_rate), video_statistics.resolution, show_classes
        ),
    )

    def iterate_file():
        with open(config.OUTPUT_FILES_PATH / "tmp.mp4", "rb") as video_file:
            yield from video_file

    return StreamingResponse(iterate_file(), media_type="video/mp4v")
