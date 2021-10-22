from dafact.encoders import Encoder, NumpyLikeEncoder, CsvEncoder
from os import PathLike
from argparse import FileType


class Dafacter:
    _encoder: Encoder = None
    _factor: int = None

    def __init__(self,
                 data,
                 feature_names=None,
                 factor=0,
                 numerical_columns=None,
                 have_names=False,
                 omit_names=False,
                 delimiter=","):
        """[summary]

        Args:
            data ([2D array-matrix or str]): data to be encoded in a 2D numpy array-like matrix or the path to a csv file.
            feature_names ([type], optional): Names of the features/columns. Will overwrite the names retrieved from the csv file in such a case. Defaults to None.
            factor (int, optional): numerical data will be multiplied by 10^factor when encoding. Defaults to 0.
            numerical_columns ([type], optional): indicates which columns store numerical data. Can be specified as a bit-array (zeros when not numerical, any other value otherwise) or as a list of indexes for the numerical columns. Defaults to None.
            have_names (bool, optional): Must be true if the csv file contains the name of the columns in the first line. Defaults to False.
            omit_names (bool, optional): Set to True if user wants to ignore the column names from the file. Defaults to False.
            delimiter (str, optional): Csv delimiter used in the csv file. Defaults to ','.
        """
        if not hasattr(data, 'shape') and (isinstance(data, (str, PathLike))):
            self._encoder = CsvEncoder(data,
                                       feature_names=feature_names,
                                       factor=factor,
                                       numerical_columns=numerical_columns,
                                       have_names=have_names,
                                       omit_names=omit_names,
                                       delimiter=delimiter)
        else:
            self._encoder = NumpyLikeEncoder(
                data,
                feature_names=feature_names,
                factor=factor,
                numerical_columns=numerical_columns,
            )
        self.data = self._encoder.data
        self.feature_names = self._encoder.feature_names
        self.as_clingo_facts = self._encoder.as_clingo_facts
        self.as_program_string = self._encoder.as_program_string
