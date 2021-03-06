import numpy as np
from scipy.optimize import linear_sum_assignment

from tsa.np_utils import iou_batch


def associate_detections_to_trackers(detections, trackers, iou_threshold: float):
    """Assigns detections to tracked object, both represented as bounding boxes.

    Returns 3 lists of matches, unmatched_detections and unmatched_trackers.

    Forked from https://github.com/abewley/sort/blob/bce9f0d1fc8fb5f45bf7084130248561a3d42f31/sort.py#L154.
    The LICENCE is the same as of our project, stated at the root level of the repository.
    """
    if len(trackers) == 0:
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5), dtype=int)

    if len(detections) == 0:
        return np.empty((0, 2), dtype=int), np.empty((0, 5), dtype=int), np.arange(len(trackers))

    iou_matrix = iou_batch(detections, trackers)

    if min(iou_matrix.shape) > 0:
        a = (iou_matrix > iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1:
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            row_indices, col_indices = linear_sum_assignment(-iou_matrix)
            matched_indices = np.array(list(zip(row_indices, col_indices)))
    else:
        matched_indices = np.empty(shape=(0, 2))

    unmatched_detections = [d for d, det in enumerate(detections) if d not in matched_indices[:, 0]]

    unmatched_trackers = [t for t, trk in enumerate(trackers) if t not in matched_indices[:, 1]]

    # filter out matched with low IOU, move them to unmatched detections and trackers
    matches = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            matches.append(m.reshape(1, 2))

    if len(matches) == 0:
        matches = np.empty((0, 2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)
        # switch positions of detections and trackers indices
        # this is to match how the columns are used in both Simple and DeepSORT
        matches = np.flip(matches, axis=1)

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)
