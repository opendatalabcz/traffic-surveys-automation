import numpy as np

from tsa.np_utils import iou_batch

from . import constants


def iou_cost(tracks, detections, track_indices, detection_indices):
    """An intersection over union distance metric.

    Parameters
    ----------
    tracks : List[deep_sort.track.Track]
        A list of tracks.
    detections : List[deep_sort.detection.Detection]
        A list of detections.
    track_indices : List[int]
        A list of indices to tracks that should be matched. Defaults to
        all `tracks`.
    detection_indices : List[int]
        A list of indices to detections that should be matched. Defaults
        to all `detections`.

    Returns
    -------
    ndarray
        Returns a cost matrix of shape
        len(track_indices), len(detection_indices) where entry (i, j) is
        `1 - iou(tracks[track_indices[i]], detections[detection_indices[j]])`.

    """
    iou_matrix = iou_batch(
        np.asarray([detection.bbox for detection in detections]),
        np.asarray([track.state for track in tracks]),
    )
    iou_matrix = iou_matrix[np.ix_(detection_indices, track_indices)]
    cost_matrix = 1.0 - iou_matrix.T

    for row, track_idx in enumerate(track_indices):
        if tracks[track_idx].time_since_update > 1:
            cost_matrix[row, :] = constants.INFINITY_COST

    return cost_matrix
