import pytest

class TestCsvEncoder:

    @pytest.fixture(scope='class')
    def fixture_example(self):
        return None

    def test_method(self, fixture_example):
        assert fixture_example is None
