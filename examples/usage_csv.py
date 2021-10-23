from dafact import Dafacter

dafacter = Dafacter("data/haberman.csv", have_names=True)
print(dafacter.as_program_string())
# print(dafacter.as_program_string(instance_func='ins',value_func='val',feature_func='f'))
