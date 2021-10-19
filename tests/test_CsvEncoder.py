from _pytest.compat import ascii_escaped
import pytest
from numpy import array, all, exp

from dafact.encoders import CsvEncoder


class TestCsvEncoder:
    @pytest.fixture(scope='class')
    def expected_data(self):
        return array([
            [30, 64, 1, 1],
            [30, 62, 3, 1],
            [30, 65, 0, 1],
        ])

    def test_constructor(self, datadir, expected_data):
        # csv with headers
        expected_features = ["age", "operation_year", "nodes", "survival"]
        csvenc = CsvEncoder((datadir / "haberman_mini.csv"), have_names=True)
        assert csvenc.feature_names == expected_features
        assert all(csvenc.data == expected_data)

        expected_manual_features = [
            "edad", "año_operación", "nódulos", "superviviencia"
        ]
        csvenc = CsvEncoder((datadir / "haberman_mini.csv"),
                            have_names=True,
                            feature_names=expected_manual_features)
        assert csvenc.feature_names == expected_manual_features

        expected_features = ["f1", "f2", "f3", "f4"]
        csvenc = CsvEncoder(
            (datadir / "haberman_mini.csv"),
            have_names=True,
            feature_names=None,
            omit_names=True,
        )
        assert csvenc.feature_names == expected_features

        # csv without headers
        expected_manual_features = [
            "edad", "año_operación", "nódulos", "superviviencia"
        ]
        csvenc = CsvEncoder((datadir / "haberman_mini_noheaders.csv"),
                            have_names=False,
                            feature_names=expected_manual_features)
        assert csvenc.feature_names == expected_manual_features

        expected_features = ["f1", "f2", "f3", "f4"]
        csvenc = CsvEncoder((datadir / "haberman_mini_noheaders.csv"),
                            have_names=False,
                            feature_names=None)
        assert csvenc.feature_names == expected_features
