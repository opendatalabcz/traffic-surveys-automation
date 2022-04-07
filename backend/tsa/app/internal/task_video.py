from starlette.responses import StreamingResponse

from tsa import processes
from tsa.datasets import VideoFramesDataset
from tsa.storage import FileStorageMethod, FrameDrawMethod


def create_video(source_video_path: str, analysis_path: str, output_frame_rate: int, show_classes: bool):
    video_generator = processes.yield_video(
        VideoFramesDataset(source_video_path, output_frame_rate, None),
        FileStorageMethod(analysis_path),
        FrameDrawMethod(source_video_path, show_classes),
    )

    return StreamingResponse(video_generator, media_type="video/mp4")
