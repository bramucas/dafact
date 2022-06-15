import pytest
from numpy import array
from clingo import Function, String, Number
from dafact import Dafacter
from numpy import all


class TestDafacter:
    @pytest.fixture(scope='class')
    def custom_data(self):
        return array([[1, 2, 3], [4, 5, 6]])

    @pytest.fixture(scope='class')
    def expected_facts(self):
        return [
            Function('feature', [String('f0')], True),
            Function('feature', [String('f1')], True),
            Function('feature', [String('f2')], True),
            Function('instance', [Number(0)], True),
            Function(
                'value',
                [Number(0), String('f0'), Number(1)], True),
            Function(
                'value',
                [Number(0), String('f1'), Number(2)], True),
            Function(
                'value',
                [Number(0), String('f2'), Number(3)], True),
            Function('instance', [Number(1)], True),
            Function(
                'value',
                [Number(1), String('f0'), Number(4)], True),
            Function(
                'value',
                [Number(1), String('f1'), Number(5)], True),
            Function(
                'value',
                [Number(1), String('f2'), Number(6)], True),
        ]

    @pytest.fixture(scope='class')
    def expected_csv_data(self):
        return array([
            [30, 64, 1, 1],
            [30, 62, 3, 1],
            [30, 65, 0, 1],
        ])

    def test_constructor_csv(self, datadir, expected_csv_data):
        dafacter = Dafacter((datadir / "haberman_mini.csv"), have_names=True)
        assert all(dafacter.data == expected_csv_data)

    def test_constructor_numpylike(self, custom_data, expected_facts):
        dafacter = Dafacter(custom_data)
        assert dafacter.as_clingo_facts() == expected_facts

    def test_constructor_numpylike(self, custom_data, expected_facts):
        dafacter = Dafacter(custom_data)
        assert dafacter.as_clingo_facts() == expected_facts
