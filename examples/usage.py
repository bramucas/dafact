from sklearn.datasets import load_iris
from dafact import Dafacter

X, _ = load_iris(return_X_y=True, as_frame=True)
dafacter = Dafacter(X, feature_names=['sep_len', 'sep_wid', 'pet_len', 'pet_wid'])
print(dafacter.as_program_string(
	factor=2,
	instance_func='ins',
	feature_func='f',
	value_func='val'
))
