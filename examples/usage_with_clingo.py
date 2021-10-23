from sklearn.datasets import load_iris
from dafact import Dafacter
from clingo import Control

# Loads data
X, _ = load_iris(return_X_y=True, as_frame=True)

# Encodes data as clingo facts
dafacter = Dafacter(X,
                    feature_names=['sep_len', 'sep_wid', 'pet_len', 'pet_wid'])
facts_plain_text = dafacter.as_program_string(factor=2,
                                              instance_func='ins',
                                              feature_func='f',
                                              value_func='val')

# Intializes clingo
clingo_ctl = Control()

# Adds the encoded facts and more
clingo_ctl.add("base", [], facts_plain_text)
clingo_ctl.add("base", [],
               'setosa(I) :- ins(I), val(I, "pet_wid", V), V < 90.')
clingo_ctl.add("base", [], '#show setosa/1.')

# Does grounding and solving
clingo_ctl.ground([("base", [])])
print(clingo_ctl.solve(on_model=print))
