from dataclasses import dataclass
from typing import cast, Optional, Tuple

import numpy as np
from shapely.geometry import LineString

from tsa import typing


class Line(LineString):
    @property
    def coordinates(self):
        return np.asarray(self.coords)
