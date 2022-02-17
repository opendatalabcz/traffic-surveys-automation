from typing import List

import cv2
import numpy as np
from sklearn.cluster import KMeans

from tsa.storage import ReadStorageMethod
from tsa.np_utils import RandomGenerator
from tsa.dataclasses.track import FinalTrack


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
