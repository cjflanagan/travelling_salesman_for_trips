import requests, json
import pandas as pd


def _get_request_string(source, dest, mode):
    """Constructing api call to Google Maps API."""
    api_key = "AIzaSyD0W2R__E7smCV5oeqQE00orlJDHhGpEAs"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
    request = (
        url
        + "origins="
        + source
        + "&destinations="
        + dest
        + "&mode="
        + mode
        + "&key="
        + api_key
    )
    return request


class DistMatrix:
    def __init__(self, source, dest, distances):
        self.source = (source,)
        self.dest = dest
        self.distances = distances

    def _create_columns(self, list_obj):
        columns = []
        for item in list_obj[0].split("|"):
            columns.append(item)
        return columns

    def _create_index(self, list_obj):
        index = []
        for item in list_obj.split("|"):
            index.append(item)
        return index

    def _create_matrix(self, list_obj, n):
        matrix = [
            list_obj[i * n : (i + 1) * n] for i in range((len(list_obj) + n - 1) // n)
        ]
        return matrix

    def _get_matrix_and_cols(self):
        columns = self._create_columns(self.source)
        matrix_raw = self._create_matrix(self.distances, len(columns))
        return matrix_raw, columns

    def get_raw_matrix(self):
        raw_matrix, columns = self._get_matrix_and_cols()
        return raw_matrix

    def create_dist_df(self):
        raw_matrix, columns = self._get_matrix_and_cols()
        print(columns)
        df = pd.DataFrame(raw_matrix)
        df.columns = columns
        df.index = self._create_index(self.dest)
        return df


def _make_request(request):
    r = requests.get(request)
    x = r.json()
    distance_json = x["rows"]
    return distance_json


def _compute_distances(distance_json):
    # bydefault driving mode considered
    distances = []
    for row in distance_json:
        for result in row["elements"]:
            distances.append(result["distance"]["value"])
    return distances


def get_distance_matrix(source, dest, mode="driving"):
    # importing required libraries
    req_string = _get_request_string(source, dest, mode)
    distance_json = _make_request(req_string)
    distances = _compute_distances(distance_json)
    matrix = DistMatrix(source, dest, distances)
    matrix = matrix.get_raw_matrix()
    return matrix
