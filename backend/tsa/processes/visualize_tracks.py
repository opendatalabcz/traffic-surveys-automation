from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from sklearn.cluster import KMeans

from tsa.dataclasses.frames import VideoFramesDataset
from tsa.dataclasses.track import FinalTrack
from tsa.np_utils import RandomGenerator
from tsa.storage import ReadStorageMethod


def _cluster_tracks(tracks: List[FinalTrack], n_clusters: int) -> List[int]:
    clustering_method = KMeans(n_clusters=n_clusters)

    return clustering_method.fit_predict(np.array([t.curve.bounds for t in tracks]))


def create_tracks_visualization(
    frame, track_source: ReadStorageMethod, minimum_path_length: float, n_clusters: int, draw_original_path: bool
):
    colors = RandomGenerator(track_source.track_name).colors(n_clusters)
    tracks = [track for track in track_source.read_track() if track.curve.length >= minimum_path_length]

    clusters = _cluster_tracks(tracks, n_clusters)

    for track, cluster in zip(tracks, clusters):
        if draw_original_path:
            for point in track.path.astype(np.int32):
                cv2.circle(frame, point, 1, colors[cluster], 2)

        cv2.polylines(frame, [track.curve.coordinates.astype(np.int32)], False, colors[cluster], 1, cv2.LINE_AA)

    return frame


def video_or_empty_frame(dataset_path: Optional[Path], resolution=(720, 1280)):
    if dataset_path:
        dataset = VideoFramesDataset(dataset_path)
        return next(dataset.frames)

    return np.zeros(resolution, dtype=np.uint8)
