import numpy as np
import pandas


class CoordinateSorter:

    def __init__(self, max_distance_delta, max_angle_delta, threshold):

        """
        Scenario: 'threshold' parameter allows to filter out noise lines
          Given: threshold = 4, set of lines
           When: sorter found 3 groups of lines
            And: the first set of lines contains 10 lines, second - 5 lines
            But: the third set of lines contains 3 lines
           Then: the third considered as noise and will not be presented in sorting result
          --
        Scenario: 'max_distance_delta' and 'max_angle_delta' parameters allow to control line group detection
          Given: 5 lines have been given to sort
            And: it is possible to create a chain 'chain_1' of lines line1, line2, line3
          Where: distance between links is less (or equal) then (max_distance_delta, max_angle_delta)
            And: it is possible to create a chain 'chain_2' of lines line4, line5
          Where: distance between links is less (or equal) then (max_distance_delta, max_angle_delta)
            And: distance between chain_1 and chain_2 edges is more than (max_distance_delta, max_angle_delta)
           Then: chain_1 and chain_2 considered as two separate lines
          --
        Resulting line is calculate as median of all lines in a group

        :param max_distance_delta: rho1 - rho2
        :param max_angle_delta: theta1 - theta2 threshold in radians
        :param threshold: min lines amount in one group
        """

        if max_angle_delta < 0:
            raise ValueError("[max_angle_delta] must be positive number")

        if max_angle_delta < 0:
            raise ValueError("[max_angle_delta] must be positive number")

        if threshold < 1 or type(threshold) != int:
            raise ValueError("[threshold] expected to be integer greater then or equal to 1")

        self._max_point_distance = (max_distance_delta, max_angle_delta)
        self._min_points_amount = threshold

    def _sortPointsByDistance(self, points_dict):
        set_list = list()

        for key, value in points_dict.items():
            indexes_set = set()
            set_list.append(indexes_set)
            indexes_set.add(key)

            for inner_key, inner_value in points_dict.items():
                point_distance = abs(np.subtract(value, inner_value))

                if point_distance[0] <= self._max_point_distance[0] \
                        and point_distance[1] <= self._max_point_distance[1]:
                    indexes_set.add(inner_key)

        return set_list

    def _splitOnGroups(self, set_list_source):

        sorted_source = list(set_list_source)
        sorted_source.sort(key=len, reverse=True)

        extremums = list()

        def find_extremums(ordered_list_of_set_items):
            if len(ordered_list_of_set_items) == 0:
                return

            first_extremum = ordered_list_of_set_items[0]
            items_for_further_sorting = list()

            for dot_set in ordered_list_of_set_items:
                if dot_set.issubset(first_extremum):
                    continue
                else:
                    if len(first_extremum.intersection(dot_set)):
                        first_extremum = first_extremum.union(dot_set)
                    else:
                        items_for_further_sorting.append(dot_set)

            extremums.append(first_extremum)
            find_extremums(items_for_further_sorting)

        find_extremums(sorted_source)

        filtered_extremums = filter(lambda x: len(x) >= self._min_points_amount, extremums)
        return filtered_extremums

    @staticmethod
    def _getMedian(source_dict, key_set):
        point_array = [source_dict[item] for item in key_set]
        data_frame = pandas.DataFrame(data=point_array, columns=["distance", "angle"])

        return data_frame["distance"].median(), data_frame["angle"].median()

    def sort(self, points_array):

        if len(points_array) < self._min_points_amount:
            return []

        points_dictionary = dict()

        for index, coordinates in enumerate(points_array):
            points_dictionary[index] = (int(coordinates[0]), coordinates[1])

        point_set_list = self._sortPointsByDistance(points_dictionary)
        point_groups = self._splitOnGroups(point_set_list)
        resulting_points = [self._getMedian(points_dictionary, point_group) for point_group in point_groups]

        return resulting_points
