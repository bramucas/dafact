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
        return array([
            [1,2,3],[4,5,6]
        ])

    @pytest.fixture(scope='class')
    def expected_facts(self):
        return [
            Function('feature',  [String('f1')], True),
            Function('feature',  [String('f2')], True),
            Function('feature',  [String('f3')], True),
            Function('instance', [Number(0)], True),
            Function('value', [Number(0), String('f1'), Number(1)], True),
            Function('value', [Number(0), String('f2'), Number(2)], True),
            Function('value', [Number(0), String('f3'), Number(3)], True),
            Function('instance', [Number(1)], True),
            Function('value', [Number(1), String('f1'), Number(4)], True),
            Function('value', [Number(1), String('f2'), Number(5)], True),
            Function('value', [Number(1), String('f3'), Number(6)], True),
        ]

    def test_constructor(self, custom_empty_data):
        # Without feature names
        enc = Encoder(custom_empty_data)

        assert all(enc.data == custom_empty_data)
        expected_feature_names = [f'f{i}' for i in range(1, custom_empty_data.shape[1]+1)]
        assert enc.feature_names == expected_feature_names

        # With feature names
        expected_feature_names = ["feature1", "feature2", "feature3", "feature4"]
        enc2 = Encoder(custom_empty_data, feature_names=expected_feature_names)
        assert enc2.feature_names == expected_feature_names

    def test_constructor_fail_feature_names_cardinality(self, custom_empty_data):
        with pytest.raises(ValueError):
            enc = Encoder(custom_empty_data, feature_names=[1])

        with pytest.raises(ValueError):
            enc = Encoder(custom_empty_data, feature_names=[1,3,4,5,5,6,7,8,9,9])

    def test_as_clingo_facts(self, custom_data, expected_facts):
        enc = Encoder(custom_data)
        assert enc.as_clingo_facts() == expected_facts
    
    def test_as_program_string(self, custom_data, datadir):
        enc = Encoder(custom_data)
        assert enc.as_program_string() == (datadir / 'expected_text.lp').read_text()
