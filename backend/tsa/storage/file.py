from pathlib import Path

import simplejson
from tsa.dataclasses.track import Track

from .abstract import WriteStorageMethod


class FileStorageMethod(WriteStorageMethod):
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
