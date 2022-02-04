from pathlib import Path
from typing import Generator

import simplejson
from tsa.dataclasses.track import FinalTrack, Track

from .abstract import ReadStorageMethod, WriteStorageMethod


class FileStorageMethod(ReadStorageMethod, WriteStorageMethod):
    def __init__(self, path: Path):
        self.output_file_path = path
        self.tracks = {}

    def save_frame(self, frame, detections, identifiers, classes, scores):
        for detection, identifier, class_, score in zip(detections, identifiers, classes, scores):
            if identifier is None:  # we don't store tracks that don't have their IDs assigned yet (not active)
                continue

            if identifier not in self.tracks:
                self.tracks[identifier] = Track(identifier)

            self.tracks[identifier].update(detection, score)

    def close(self):
        with open(self.output_file_path, "w", encoding="utf-8") as output_file:
            simplejson.dump([track.as_dict() for track in self.tracks.values()], output_file)

    def read_track(self) -> Generator[FinalTrack, None, None]:
        with open(self.output_file_path, "r", encoding="utf-8") as input_file:
            all_tracks = simplejson.load(input_file)

        for track in all_tracks:
            yield FinalTrack(track)
