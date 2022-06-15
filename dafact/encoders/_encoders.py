from clingo import Function, String, Number
import csv
from numpy import asarray, genfromtxt, zeros, ones


class Encoder:
    def __init__(self,
                 data,
                 feature_names=None,
                 numerical_columns=None,
                 factor: int = 0):
        """WARNING: this class is not intended to be instanciated. Use a child class instead.

        Args:
            data ([np.ndarray]): should be 2-dimensional.
            feature_names ([Iterable[str]], optional): name of the columns. If None, default names (f1, f2, etc.) will be given: Defaults to None.
            numerical_columns (Iterable[int], optional): indexes of the columns which are meant to be treated as numerical. If None, all columns will be treated as numerical. Can be given as a bit array (zero for non numerical columns, anything otherwise) or as a list of indexes. Defaults to None.
            factor ([int], optinal): if not None, numerical data will be multiplyed by 10^factor and then rounded. Defaults to None.

        Raises:
            ValueError: if feature_names length does not match the shape of data.
        """
        if feature_names is None:
            feature_names = [f'f{i}' for i in range(data.shape[1])]
        elif len(feature_names) != data.shape[1]:
            raise ValueError("'feature_names' len does not match data shape.")

        if numerical_columns is None:
            self._numerical_columns = ones((data.shape[1]))
        else:
            if len(numerical_columns) == data.shape[1]:
                self._numerical_columns = numerical_columns
            else:
                self._numerical_columns = zeros((data.shape[1], ))
                for i in numerical_columns:
                    self._numerical_columns[i] = 1

        if type(factor) != int:
            raise ValueError("'factor' must be int.")

        self.data = data
        self.feature_names = feature_names
        self.factor = factor

        self._facts_cache = None
        self._text_cache = None
        self._last_call = (None, None, None, None, None)

    def _check_facts_cache(self, feature_names, factor, instance_func,
                           feature_func, value_func):
        return (self._facts_cache is not None) \
            and self._last_call == (feature_names, factor, instance_func, feature_func, value_func)

    def _check_text_cache(self, feature_names, factor, instance_func,
                          feature_func, value_func):
        return (self._text_cache is not None) \
            and self._last_call == (feature_names, factor, instance_func, feature_func, value_func)

    def _get_feature_names(self, feature_names):
        if feature_names is None:
            return self.feature_names
        elif len(feature_names) != self.data.shape[1]:
            raise ValueError("'feature_names' len does not match data shape.")
        else:
            return feature_names

    def as_clingo_facts(self,
                        feature_names=None,
                        factor=None,
                        instance_func='instance',
                        feature_func='feature',
                        value_func='value'):
        """Returns the data as clingo Function objects. Includes one function identifying
        each instance, one function identifying each feature name,  and one function for 
        each instance's value.

        Numerical data is multiplied by 10^factor and then rounded, before being encoded into ASP facts.

        Args:
            feature_names ([Iterable[str]], optional): feature names to be used. If None, the feature names specified when creating the object will be used. Defaults to None.
            factor ([int], optinal): numerical data will be multiplied by 10^factor and then rounded. When None, the factor used when creating the object will be used. Defaults to None.
            instance_func (str, optional): name for the function used for identifying each instance. Defaults to 'instance'.
            feature_func (str, optional): name for the function used for identifying each feature. Defaults to 'feature'.
            value_func (str, optional): name for the function used for encoding each value. Defaults to 'value'.

        Returns:
            [Iterable[clingo.Function]]: an iterable over clingo Function objects representing the data.
        """
        feature_names = self._get_feature_names(feature_names)
        if factor is None:
            factor = self.factor
        mult = 10**factor

        # Check cache
        if self._check_facts_cache(feature_names, factor, instance_func,
                                   feature_func, value_func):
            return self._facts_cache

        # Feature facts
        clingo_facts = [
            Function(feature_func, [String(fname)], True)
            for fname in feature_names
        ]
        # Instance and Value facts
        n_rows, _ = self.data.shape
        for i in range(n_rows):
            clingo_facts.append(Function(instance_func, [Number(i)]))
            clingo_facts.extend([
                Function(value_func, [
                    Number(i),
                    String(fname),
                    Number(int(round(val * mult))) if numerical else Number(
                        int(val)),
                ], True) for fname, numerical, val in zip(
                    feature_names, self._numerical_columns, self.data[i])
            ])

        # Set cache
        self._facts_cache = clingo_facts
        self._last_call = (feature_names, factor, instance_func, feature_func,
                           value_func)

        return self._facts_cache

    def as_program_string(self,
                          feature_names=None,
                          factor=None,
                          instance_func='instance',
                          feature_func='feature',
                          value_func='value'):
        """Returns the data as a ASP program in a string. Includes one function identifying
        each instance, one function identifying each feature name,  and one function for 
        each instance's value.

        Numerical data is multiplied by 10^factor and then rounded, before being encoded into ASP facts.

        Args:
            feature_names ([Iterable[str]], optional): feature names to be used. If None, the feature names specified when creating the object will be used. Defaults to None.
            factor ([int], optinal): numerical data will be multiplied by 10^factor and then rounded. When None, the factor used when creating the object will be used. Defaults to None.
            instance_func (str, optional): name for the function used for identifying each instance. Defaults to 'instance'.
            feature_func (str, optional): name for the function used for identifying each feature. Defaults to 'feature'.
            value_func (str, optional): name for the function used for encoding each value. Defaults to 'value'.

        Returns:
            [str]: a string containig the data encoded as an ASP program.
        """
        def fact_lines(feature_names, clingo_facts):
            len_features = len(feature_names)
            len_rows = len_features + 1
            yield clingo_facts[0:len_features]
            for i in range(len_features, len(clingo_facts), len_rows):
                yield clingo_facts[i:i + len_rows]

        feature_names = self._get_feature_names(feature_names)
        if factor is None:
            factor = self.factor

        if self._check_text_cache(feature_names, factor, instance_func,
                                  feature_func, value_func):
            return self._text_cache

        clingo_facts = self.as_clingo_facts(feature_names=feature_names,
                                            factor=factor,
                                            instance_func=instance_func,
                                            feature_func=feature_func,
                                            value_func=value_func)
        self._text_cache = "\n".join(
            " ".join([str(f) + "." for f in list])
            for list in fact_lines(feature_names, clingo_facts))
        return self._text_cache


class CsvEncoder(Encoder):
    def __init__(self,
                 csv_path,
                 feature_names=None,
                 factor=0,
                 numerical_columns=None,
                 have_names=False,
                 omit_names=False,
                 delimiter=','):
        """Encodes a csv file as a set of ASP facts. If no feature_names are provided (neither manually or from the csv file), they will be automatically created as 'f1', 'f2', etc. Behaviour is not controlled when 'have_names' setted accordingly.

        Args:
            csv_path ([str]): path to the csv file.
            feature_names (Iterable[str], optional): Names of the features/columns. Will overwrite the names retrieved from the file in such a case. Defaults to None.
            have_names (bool, optional): Must be true if the csv file contains the name of the columns in the first line. Defaults to False.
            omit_names (bool, optional): Set to True if user wants to ignore the column names from the file. Defaults to False.
            delimiter (str, optional): Csv delimiter used in the csv file. Defaults to ','.
        """
        if have_names == False:  # csv do not have headers
            data = genfromtxt(csv_path, delimiter=delimiter)
        else:
            data = genfromtxt(csv_path, skip_header=1, delimiter=delimiter)
            if feature_names is None and omit_names == False:  # and names==True
                with open(csv_path, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=delimiter)
                    feature_names = next(reader)

        super().__init__(data,
                         feature_names=feature_names,
                         factor=factor,
                         numerical_columns=numerical_columns)


class NumpyLikeEncoder(Encoder):
    def __init__(self,
                 data,
                 feature_names=None,
                 factor=0,
                 numerical_columns=None):
        """Encodes a (2D matrix) numpy array-like variable as a set of ASP Facts. Any type which accepts np.asarray(var) should work. If no feature_names are provided, they will be automatically created as 'f1', 'f2', etc.

        Args:
            data (2d matrix): data to be encoded.
            feature_names (Iterable[str], optional): Names for the features/columns. Defaults to None.
        """
        if feature_names is None and hasattr(data, 'columns'):
            feature_names = list(data.columns)
        super().__init__(asarray(data),
                         feature_names=feature_names,
                         factor=factor,
                         numerical_columns=numerical_columns)
