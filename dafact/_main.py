from dafact.encoders import Encoder, NumpyLikeEncoder, CsvEncoder
from os import PathLike


class Dafacter:
    _encoder: Encoder = None

    def __init__(self,
                 data,
                 feature_names=None,
                 have_names=False,
                 omit_names=False,
                 delimiter=","):
        """

        Args:
            data ([type]): [description]
            feature_names ([type], optional): [description]. Defaults to None.
            have_names (bool, optional): [description]. Defaults to False.
            omit_names (bool, optional): [description]. Defaults to False.
            delimiter (str, optional): [description]. Defaults to ",".
        """
        if not hasattr(data, 'shape') and (isinstance(data, str)
                                           or isinstance(data, PathLike)):
            self._encoder = CsvEncoder(data,
                                       feature_names=feature_names,
                                       have_names=have_names,
                                       omit_names=omit_names,
                                       delimiter=delimiter)
        else:
            self._encoder = NumpyLikeEncoder(data, feature_names=feature_names)
        self.data = self._encoder.data
        self.feature_names = self._encoder.feature_names
        self.as_clingo_facts = self._encoder.as_clingo_facts
        self.as_program_string = self._encoder.as_program_string
