import cv2
import numpy as np

from tsa.storage import ReadStorageMethod
from tsa.np_utils import generate_color


def create_tracks_visualization(frame, track_source: ReadStorageMethod, draw_original_path):
    for track in track_source.read_track():
        color = generate_color()
        poly_line = np.asarray([track.interpolation(x) for x in track.interpolation.x_lin_space])

        if draw_original_path:
            for point in track.path.astype(np.int32):
                cv2.circle(
                    frame,
                    point,
                    1,
                    color,
                    2,
                )

        cv2.polylines(
            frame,
            [poly_line.astype(np.int32)],
            False,
            color,
            2,
        )

    return frame
