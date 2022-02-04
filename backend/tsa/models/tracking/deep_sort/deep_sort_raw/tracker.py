from typing import List

import numpy as np

from tsa.models.tracking.tracker import DeepTracker as Track

from . import linear_assignment
from . import iou_matching
from .detection import Detection


class Tracker:
    """
    This is the multi-target tracker.

    Parameters
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        A distance metric for measurement-to-track association.
    max_age : int
        Maximum number of missing detections before a track is deleted.
    n_init : int
        Number of consecutive detections before the track is confirmed. The
        track state is set to `Deleted` if a miss occurs within the first
        `n_init` frames.

    Attributes
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        The distance metric used for measurement to track association.
    max_age : int
        Maximum number of missing detections before a track is deleted.
    n_init : int
        Number of frames that a track remains in initialization phase.
    tracks : List[Track]
        The list of active tracks at the current time step.

    """

    def __init__(self, metric, max_iou_distance, max_age, n_init):
        self.metric = metric
        self.max_iou_distance = max_iou_distance
        self.max_age = max_age
        self.n_init = n_init

        self.tracks: List[Track] = []

    def predict(self):
        """Propagate track state distributions one time step forward.

        This function should be called once every time step, before `update`.
        """
        return np.asarray([tracker.predict() for tracker in self.tracks])

    def update(self, matches, unmatched_tracks, unmatched_detections, detections: List[Detection]):
        """Perform measurement update and track management."""
        # Update track set
        for track_idx, detection_idx in matches:
            self.tracks[track_idx].update_with_feature(
                detections[detection_idx].bbox, detections[detection_idx].feature
            )
        for track_idx in unmatched_tracks:
            self.tracks[track_idx].mark_missed()
        for detection_idx in unmatched_detections:
            self._initiate_track(detections[detection_idx])

        # Delete expired tracks
        for i in reversed(range(len(self.tracks))):
            if self.tracks[i].is_deleted:
                self.tracks.pop(i)

        # Update distance metric
        active_targets = [t.id for t in self.tracks if t.is_active]
        features, targets = [], []
        for track in self.tracks:
            if not track.is_active:
                continue
            features += track.features
            targets += [track.id for _ in track.features]
            track.features = []

        self.metric.partial_fit(np.asarray(features), np.asarray(targets), active_targets)

    def match(self, detections):
        def gated_metric(tracks, dets, track_indices, detection_indices):
            features = np.array([dets[i].feature for i in detection_indices])
            targets = np.array([tracks[i].id for i in track_indices])
            cost_matrix = self.metric.distance(features, targets)
            cost_matrix = linear_assignment.gate_cost_matrix(
                cost_matrix, tracks, dets, track_indices, detection_indices
            )

            return cost_matrix

        # Split track set into confirmed and unconfirmed tracks.
        confirmed_tracks = [i for i, t in enumerate(self.tracks) if t.is_active]
        unconfirmed_tracks = [i for i, t in enumerate(self.tracks) if not t.is_active]

        # Associate confirmed tracks using appearance features.
        matches_a, unmatched_tracks_a, unmatched_detections = linear_assignment.matching_cascade(
            gated_metric, self.metric.matching_threshold, self.max_age, self.tracks, detections, confirmed_tracks
        )

        # Associate remaining tracks together with unconfirmed tracks using IOU.
        iou_track_candidates = unconfirmed_tracks + [
            k for k in unmatched_tracks_a if self.tracks[k].time_since_update == 1
        ]
        unmatched_tracks_a = [k for k in unmatched_tracks_a if self.tracks[k].time_since_update != 1]
        matches_b, unmatched_tracks_b, unmatched_detections = linear_assignment.min_cost_matching(
            iou_matching.iou_cost,
            self.max_iou_distance,
            self.tracks,
            detections,
            iou_track_candidates,
            unmatched_detections,
        )

        matches = matches_a + matches_b
        unmatched_tracks = list(set(unmatched_tracks_a + unmatched_tracks_b))

        return matches, unmatched_tracks, unmatched_detections

    def _initiate_track(self, detection: Detection):
        new_tracker = Track(detection.bbox, self.n_init, self.max_age, detection.feature)
        self.tracks.append(new_tracker)
