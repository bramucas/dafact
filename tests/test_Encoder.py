import pytest
from numpy import zeros, all
from dafact.encoders import Encoder

class TestEncoder:

    @pytest.fixture(scope='class')
    def custom_data(self):
        return zeros((3, 4))

    def test_constructor(self, custom_data):
        # Without feature names
        be = Encoder(custom_data)

        assert all(be.data == custom_data)
        expected_feature_names = [f'f{i}' for i in range(1, custom_data.shape[1]+1)]
        assert be.feature_names == expected_feature_names

        # With feature names
        expected_feature_names = ["feature1", "feature2", "feature3", "feature4"]
        be2 = Encoder(custom_data, feature_names=expected_feature_names)
        assert be2.feature_names == expected_feature_names

    def test_constructor_fail_feature_names_cardinality(self, custom_data):
        with pytest.raises(ValueError):
            be = Encoder(custom_data, feature_names=[1])

        with pytest.raises(ValueError):
            be = Encoder(custom_data, feature_names=[1,3,4,5,5,6,7,8,9,9])
