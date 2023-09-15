from clingo.symbol import Function
import pytest
from numpy import array
from dafact.encoders import NumpyLikeEncoder
from clingo import Function, String, Number

class TestNumpyLikeEncoder:

    @pytest.fixture(scope='class')
    def custom_data(self):
        return array([
            [1,2,3],[4,5,6]
        ])

    @pytest.fixture(scope='class')
    def expected_facts(self):
        return [
            Function('feature',  [Number(0), String('f0')], True),
            Function('feature',  [Number(1), String('f1')], True),
            Function('feature',  [Number(2), String('f2')], True),
            Function('instance', [Number(0)], True),
            Function('value', [Number(0), Number(0), Number(1)], True),
            Function('value', [Number(0), Number(1), Number(2)], True),
            Function('value', [Number(0), Number(2), Number(3)], True),
            Function('instance', [Number(1)], True),
            Function('value', [Number(1), Number(0), Number(4)], True),
            Function('value', [Number(1), Number(1), Number(5)], True),
            Function('value', [Number(1), Number(2), Number(6)], True),
        ]

    def test_as_clingo_facts(self, custom_data, expected_facts):
        npenc = NumpyLikeEncoder(custom_data)
        assert npenc.as_clingo_facts() == expected_facts
    
    def test_as_program_string(self, custom_data, datadir):
        npenc = NumpyLikeEncoder(custom_data)
        assert npenc.as_program_string() == (datadir / 'expected_text.lp').read_text()
 