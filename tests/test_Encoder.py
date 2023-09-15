from _pytest.fixtures import pytest_sessionstart
import pytest
from numpy import zeros, all, array
from clingo import Function, String, Number
from dafact.encoders import Encoder


class TestEncoder:
    @pytest.fixture(scope='class')
    def custom_empty_data(self):
        return zeros((3, 4))

    @pytest.fixture(scope='class')
    def custom_data(self):
        return array([[1, 2, 3], [4, 5, 6]])

    @pytest.fixture(scope='class')
    def custom_decimal_data(self):
        return array([[25.566, 30.4, 9.993384, 1], [22.001, 28.453, 9.9384,
                                                    0]])

    @pytest.fixture(scope='class')
    def expected_facts_factor_3(self):
        return [
            Function('feature', [Number(0), String('f0')], True),
            Function('feature', [Number(1), String('f1')], True),
            Function('feature', [Number(2), String('f2')], True),
            Function('feature', [Number(3), String('f3')], True),
            Function('instance', [Number(0)], True),
            Function('value',
                     [Number(0), Number(0),
                      Number(25566)], True),
            Function('value',
                     [Number(0), Number(1),
                      Number(30400)], True),
            Function('value',
                     [Number(0), Number(2),
                      Number(9993)], True),
            Function(
                'value',
                [Number(0), Number(3), Number(1)], True),
            Function('instance', [Number(1)], True),
            Function('value',
                     [Number(1), Number(0),
                      Number(22001)], True),
            Function('value',
                     [Number(1), Number(1),
                      Number(28453)], True),
            Function('value',
                     [Number(1), Number(2),
                      Number(9938)], True),
            Function(
                'value',
                [Number(1), Number(3), Number(0)], True),
        ]

    @pytest.fixture(scope='class')
    def expected_facts(self):
        return [
            Function('feature', [Number(0), String('f0')], True),
            Function('feature', [Number(1), String('f1')], True),
            Function('feature', [Number(2), String('f2')], True),
            Function('instance', [Number(0)], True),
            Function(
                'value',
                [Number(0), Number(0), Number(1)], True),
            Function(
                'value',
                [Number(0), Number(1), Number(2)], True),
            Function(
                'value',
                [Number(0), Number(2), Number(3)], True),
            Function('instance', [Number(1)], True),
            Function(
                'value',
                [Number(1), Number(0), Number(4)], True),
            Function(
                'value',
                [Number(1), Number(1), Number(5)], True),
            Function(
                'value',
                [Number(1), Number(2), Number(6)], True),
        ]

    @pytest.fixture(scope='class')
    def expected_facts_factor_0(self):
        return [
            Function('feature', [Number(0),String('f0')], True),
            Function('feature', [Number(1),String('f1')], True),
            Function('feature', [Number(2),String('f2')], True),
            Function('feature', [Number(3),String('f3')], True),
            Function('instance', [Number(0)], True),
            Function(
                'value',
                [Number(0), Number(0), Number(26)], True),
            Function(
                'value',
                [Number(0), Number(1), Number(30)], True),
            Function(
                'value',
                [Number(0), Number(2), Number(10)], True),
            Function(
                'value',
                [Number(0), Number(3), Number(1)], True),
            Function('instance', [Number(1)], True),
            Function(
                'value',
                [Number(1), Number(0), Number(22)], True),
            Function(
                'value',
                [Number(1), Number(1), Number(28)], True),
            Function(
                'value',
                [Number(1), Number(2), Number(10)], True),
            Function(
                'value',
                [Number(1), Number(3), Number(0)], True),
        ]

    def test_constructor(self, custom_empty_data, custom_decimal_data,
                         expected_facts_factor_0, expected_facts_factor_3):
        # Without feature names
        enc = Encoder(custom_empty_data)

        assert all(enc.data == custom_empty_data)
        expected_feature_names = [
            f'f{i}' for i in range(custom_empty_data.shape[1])
        ]
        assert enc.feature_names == expected_feature_names

        # With feature names
        expected_feature_names = [
            "feature1", "feature2", "feature3", "feature4"
        ]
        enc2 = Encoder(custom_empty_data, feature_names=expected_feature_names)
        assert enc2.feature_names == expected_feature_names

        # Decimals factor 0
        enc3 = Encoder(custom_decimal_data, numerical_columns=[1, 1, 1, 0])
        assert enc3.as_clingo_facts() == expected_facts_factor_0

        # Decimals factor 3
        enc3 = Encoder(custom_decimal_data,
                       factor=3,
                       numerical_columns=[1, 1, 1, 0])
        assert enc3.as_clingo_facts() == expected_facts_factor_3

        # Numerical columns specified as indexes
        enc3 = Encoder(custom_decimal_data,
                       factor=3,
                       numerical_columns=[0, 1, 2])
        assert enc3.as_clingo_facts() == expected_facts_factor_3

    def test_constructor_fail_feature_names_cardinality(
            self, custom_empty_data):
        with pytest.raises(ValueError):
            enc = Encoder(custom_empty_data, feature_names=[1])

        with pytest.raises(ValueError):
            enc = Encoder(custom_empty_data,
                          feature_names=[1, 3, 4, 5, 5, 6, 7, 8, 9, 9])

    def test_constructor_fail_numerical_columns_bad_index(
            self, custom_empty_data):
        with pytest.raises(IndexError):
            enc = Encoder(custom_empty_data, numerical_columns=[39, 2, 0])

    def test_as_clingo_facts(self, custom_data, expected_facts):
        enc = Encoder(custom_data)
        assert enc.as_clingo_facts() == expected_facts

    def test_as_program_string(self, custom_data, datadir):
        # Default feature names
        enc = Encoder(custom_data)
        assert enc.as_program_string() == (datadir /
                                           'expected_text.lp').read_text()

        # Other feature names, diff cache
        assert enc.as_program_string(
            feature_names=["hola", "buenas", "tardes"]) == (
                datadir / 'expected_text2.lp').read_text()
