from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Generator

import simplejson

from tsa.config import config
from tsa.dataclasses.track import FinalTrack, Track

from .abstract import ReadStorageMethod, WriteStorageMethod


class FileStorageMethod(ReadStorageMethod, WriteStorageMethod):
    def __init__(self, path: Path):
        self.frame_counter = 0
        self.output_file_path = path
        self.tracks: Dict[str, Track] = {}

    def save_frame(self, _, detections, identifiers, classes, scores):
        for detection, identifier, class_, score in zip(detections, identifiers, classes, scores):
            if identifier is None:  # we don't store tracks that don't have their IDs assigned yet (not active)
                continue

            if identifier not in self.tracks:
                self.tracks[identifier] = Track(identifier, int(class_.numpy()))

            self.tracks[identifier].update(self.frame_counter, detection, score)

        self.frame_counter += 1

    def close(self):
        with self._open_output_path("w") as output_file:
            simplejson.dump(
                [
                    track.as_dict()
                    for track in self.tracks.values()
                    if track.count >= config.INTERPOLATION_POLYNOMIAL_DEGREE + 1
                ],
                output_file,
            )

    @property
    def track_name(self) -> str:
        return str(self.output_file_path)

    def read_track(self) -> Generator[FinalTrack, None, None]:
        with self._open_output_path("r") as input_file:
            all_tracks = simplejson.load(input_file)

        for track in all_tracks:
            yield FinalTrack(track)

    @contextmanager
    def _open_output_path(self, method: str):
        with open(self.output_file_path, method, encoding="utf-8") as input_file:
            yield input_file
