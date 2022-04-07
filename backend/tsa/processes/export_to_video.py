from collections import defaultdict
from typing import Dict, List

from tsa import typing
from tsa.datasets import FramesDataset
from tsa.storage import ReadStorageMethod, WriteStorageMethod, FrameStorageMethod
from tsa.dataclasses.track import FinalTrack


def _build_mapping(track_source: ReadStorageMethod) -> Dict[int, List[FinalTrack]]:
    track_mapping = defaultdict(list)

    for track in track_source.read_track():
        for frame_number in track.frame_numbers:
            track_mapping[frame_number].append(track)

    return track_mapping


def _tracks_to_data(tracks: List[FinalTrack], frame_number: int):
    detections, identifiers, scores, classes = [], [], [], []

    for track in tracks:
        detections.append(track.bounding_box(frame_number))
        identifiers.append(track.identifier)
        scores.append(track.average_score)
        classes.append(track.class_)

    return detections, identifiers, classes, scores


def export_to_video(
    video: FramesDataset,
    track_source: ReadStorageMethod,
    video_destination: WriteStorageMethod,
):
    frame_track_mapping = _build_mapping(track_source)

    for i, frame in enumerate(video.frames):
        tracks_in_frame = frame_track_mapping.get(i)

        if tracks_in_frame is None:
            continue

        video_destination.save_frame(frame, *_tracks_to_data(tracks_in_frame, i))

    video_destination.close()


def yield_video(
    video: FramesDataset, track_source: ReadStorageMethod, video_destination: FrameStorageMethod
) -> typing.FRAME_GENERATOR:
    frame_track_mapping = _build_mapping(track_source)

    for i, frame in enumerate(video.frames):
        tracks_in_frame = frame_track_mapping.get(i)

        if tracks_in_frame is not None:
            yield from video_destination.draw_objects(frame, *_tracks_to_data(tracks_in_frame, i))
