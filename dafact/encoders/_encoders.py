from clingo import Function, String, Number
import clingo
from numpy import asarray, isscalar, string_
from typing import Iterable

class Encoder:
    def __init__(self, data, feature_names=None):
        if feature_names is None:
            feature_names = [f'f{i}' for i in range(1, data.shape[1]+1)]
        elif len(feature_names) != data.shape[1]:
            raise ValueError("'feature_names' len does not match data shape.")

        self.data = data
        self.feature_names = feature_names

        self._facts_cache=None
        self._text_cache=None
        self._last_call=(None,None,None,None)

    def _check_facts_cache(self, feature_names, instance_func, feature_func, value_func):
        return (self._facts_cache is not None) \
            and self._last_call == (feature_names, instance_func, feature_func, value_func)

    def _check_text_cache(self, feature_names, instance_func, feature_func, value_func):
        return (self._text_cache is not None) \
            and self._last_call == (feature_names, instance_func, feature_func, value_func)

    def _get_feature_names(self, feature_names):
        if feature_names is None:
            return self.feature_names
        elif len(feature_names) != self.data.shape[1]:
            raise ValueError("'feature_names' len does not match data shape.")
        else:
            return feature_names

    def as_clingo_facts(self, feature_names=None, instance_func='instance', feature_func='feature', value_func='value'):
        raise NotImplementedError

    def as_program_string(self, feature_names=None, instance_func='instance', feature_func='feature', value_func='value'):
        raise NotImplementedError

class CsvEncoder(Encoder):
    pass

class NumpyLikeEncoder(Encoder):
    def __init__(self, data, feature_names=None):
        if feature_names is None and hasattr(data, 'columns'):
            feature_names = data.columns
        super().__init__(asarray(data), feature_names)
    
    def as_clingo_facts(self, feature_names=None, instance_func='instance', feature_func='feature', value_func='value'):
        feature_names = self._get_feature_names(feature_names)

        # Check cache
        if self._check_facts_cache(feature_names, instance_func, feature_func, value_func):
            return self._facts_cache

        # Feature facts
        clingo_facts = [Function(feature_func, [String(fname)], True) for fname in self.feature_names]
        # Instance and Value facts
        n_rows, _ = self.data.shape
        for i in range(n_rows):
            clingo_facts.append(Function(instance_func, [Number(i)]))
            clingo_facts.extend(
                [Function(
                    value_func, 
                    [Number(i), String(fname), Number(val) if isscalar(val) else String(val)],
                    True
                )
                for fname, val in zip(self.feature_names, self.data[i])]
            )
        
        # Set cache
        self._facts_cache = clingo_facts
        self._last_call = (feature_names, instance_func, feature_func, value_func)

        return self._facts_cache

    def as_program_string(self, feature_names=None, instance_func='instance', feature_func='feature', value_func='value'):
        def fact_lines(feature_names, clingo_facts):
            len_features = len(feature_names)
            len_rows = len_features + 1
            yield clingo_facts[0:len_features]
            for i in range(len_features, len(clingo_facts), len_rows):
                yield clingo_facts[i:i + len_rows]

        feature_names = self._get_feature_names(feature_names)
        
        if self._check_text_cache(feature_names, instance_func, feature_func, value_func):
            return self._text_cache
        
        clingo_facts = self.as_clingo_facts(feature_names, instance_func, feature_func, value_func)
        self._text_cache = "\n".join(
            " ".join(
                [str(f)+"." for f in list]
            ) 
            for list in fact_lines(feature_names, clingo_facts)
        )
        return self._text_cache       
