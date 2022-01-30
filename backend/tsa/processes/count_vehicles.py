from operator import itemgetter
from typing import List

import numpy as np

from tsa.dataclasses.geometry.line import Line
from tsa.storage import ReadStorageMethod


def _order_intersection_indices(track, intersections):
    if len(intersections) == 2:
        if track.curve.angle(Line([intersections[0][1], intersections[1][1]])) <= 90.0:
            return tuple(map(itemgetter(0), intersections))

        return tuple(map(itemgetter(0), reversed(intersections)))

    if len(intersections) == 1:
        return intersections[0][0], -1

    return None


def count_vehicles(track_source: ReadStorageMethod, count_lines: List[Line]):
    number_of_lines = len(count_lines)
    counts = np.zeros((number_of_lines, number_of_lines + 1), dtype=np.int32)

    for track in track_source.read_track():
        intersections = []

        for i, line in enumerate(count_lines):
            intersection_point = track.curve.intersection(line)

            if not intersection_point.is_empty:
                intersections.append((i, intersection_point))

        if not intersections:
            continue

        from_index, to_index = _order_intersection_indices(track, intersections)
        counts[from_index, to_index] += 1

    return counts
