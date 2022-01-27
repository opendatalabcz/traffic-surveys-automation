from typing import List

import cv2
import numpy as np
from sklearn.cluster import KMeans

from tsa.storage import ReadStorageMethod
from tsa.np_utils import generate_color
from tsa.dataclasses.track import Track


def _cluster_tracks(tracks: List[Track], n_clusters: int) -> List[int]:
    clustering_method = KMeans(n_clusters=n_clusters)

    return clustering_method.fit_predict(
        np.array([np.concatenate((t.smooth_path.start_point, t.smooth_path.end_point)) for t in tracks])
    )


def create_tracks_visualization(
    frame, track_source: ReadStorageMethod, minimum_path_length: float, n_clusters: int, draw_original_path: bool
):
    tracks = [track for track in track_source.read_track() if track.smooth_path_length >= minimum_path_length]
    colors = [generate_color() for _ in range(n_clusters)]

    clusters = _cluster_tracks(tracks, n_clusters)

    for track, cluster in zip(tracks, clusters):
        if draw_original_path:
            for point in track.path.astype(np.int32):
                cv2.circle(frame, point, 1, colors[cluster], 2)

        cv2.polylines(frame, [track.smooth_path.points(100).astype(np.int32)], False, colors[cluster], 2)

    return frame
