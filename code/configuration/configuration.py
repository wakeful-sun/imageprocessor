import numpy as np
import json
import os

def getPathFor(file_path):
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, file_path)

class HoughTransformConfig:

    def __init__(self):
        with open(getPathFor("config.json")) as settings_source:
            data = json.load(settings_source)

            self._rho = data["houghTransformConfig"]["rho"]#2
            self._theta = data["houghTransformConfig"]["theta"]#2
            self._min_intersection_amount = data["houghTransformConfig"]["min_intersection_amount"]#70
            self._min_line_length = data["houghTransformConfig"]["min_line_length"]#30
            self._max_line_gap = data["houghTransformConfig"]["max_line_gap"]#10


    def rho(self):
        return self._rho

    def theta(self):
        return (np.pi / 180) * self._theta

    def min_intersection_amount(self):
        return self._min_intersection_amount

    def min_line_length(self):
        return self._min_line_length

    def max_line_gap(self):
        return self._max_line_gap