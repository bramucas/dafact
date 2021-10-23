# Usage

This document provide with examples on how to use dafacter to encode different sources of data into ASP facts.

## Python Dafacter class: basic usage
```Dafacter``` class provides all the funcionality. Once fed with data, a ```Dafacter``` object provides two main methods for obtaining a logic program:
```python
from dafact import Dafacter
dafacter = Dafacter("data/haberman.csv", have_names=True) # Fed data into the object
clingo_facts = dafacter.as_clingo_facts()  # Returns a list of clingo.Function objects
program_text = dafacter.as_program_string()  # Returns the program as plain text
```

The ```Dafacter``` class accepts multiple type of data sources and provides some options for personalizing the resulting encoding. More detail in examples below.

The following piece of code loads the [haberman](https://www.kaggle.com/gilsousa/habermans-survival-data-set) dataset from a csv file and encodes it as a logic program.
```python
# examples/usage_csv.py
from dafact import Dafacter

dafacter = Dafacter("data/haberman.csv", have_names=True)
print(dafacter.as_program_string())
```

The result of that code would be:

```
feature("age"). feature("op_year"). feature("nodes"). feature("survival").
instance(0). value(0,"age",30). value(0,"op_year",64). value(0,"nodes",1). value(0,"survival",1).
instance(1). value(1,"age",30). value(1,"op_year",62). value(1,"nodes",3). value(1,"survival",1).
(. . .)
```

## Tweaking the encoding
The encoded style can also be tweaked easily:
```python
from dafact import Dafacter

dafacter = Dafacter("data/haberman.csv", have_names=True)
print(dafacter.as_program_string(instance_func='ins',value_func='val',feature_func='f'))
```
```
f("age"). f("op_year"). f("nodes"). f("survival").
ins(0). val(0,"age",30). val(0,"op_year",64). val(0,"nodes",1). val(0,"survival",1).
ins(1). val(1,"age",30). val(1,"op_year",62). val(1,"nodes",3). val(1,"survival",1).
(. . .)
```

## Multiple kind of data sources
```Dafacter``` class accepts different kind of data sources from [numpy](https://github.com/numpy/numpy) arrays to [pandas](https://github.com/pandas-dev/pandas) DataFrames.

The next piece of code loads the iris dataset from [sklearn](https://github.com/scikit-learn/scikit-learn) library as a pandas DataFrame and directly creates a ```Dafacter``` from it. It also overwrites the original feature names with a short version of them.

```python
# examples/usage.py
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
```
```
f("sep_len"). f("sep_wid"). f("pet_len"). f("pet_wid").
ins(0). val(0,"sep_len",510). val(0,"sep_wid",350). val(0,"pet_len",140). val(0,"pet_wid",20).
ins(1). val(1,"sep_len",490). val(1,"sep_wid",300). val(1,"pet_len",140). val(1,"pet_wid",20).
ins(2). val(2,"sep_len",470). val(2,"sep_wid",320). val(2,"pet_len",130). val(2,"pet_wid",20).
```

## Integration with clingo

The following piece of code loads the iris dataset into clingo and then adds a rule for identifying which instances are a setosa flower.

```python
# examples/usage_with_clingo.py
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
```

## Usage of the command line interface

Once installed through ```pip``` users can use ```dafact``` for directly obtain a logic program from csv files through the use of the command line tool. The usage of the tool is the same to the use of the ```Dafacter``` python class for csv files.

```
~/$ dafact --help
usage: dafact [-h] [--feature-names [FEATURE_NAMES [FEATURE_NAMES ...]]] [--factor FACTOR]
              [--numerical-columns [NUMERICAL_COLUMNS [NUMERICAL_COLUMNS ...]]] [--have-names] [--omit-names] [--delimiter DELIMITER]
              infile outfile

Dafact CLI Encodes data as ASP facts.

positional arguments:
  infile                Input csv file.
  outfile               Ouput ASP program.

optional arguments:
  -h, --help            show this help message and exit

Options:
  --feature-names [FEATURE_NAMES [FEATURE_NAMES ...]]
                        Feature names for the csv columns.
  --factor FACTOR       factor help
  --numerical-columns [NUMERICAL_COLUMNS [NUMERICAL_COLUMNS ...]]
                        Indexes for numerical columns.
  --have-names          Must be if csv have the name of the columns in the first line.
  --omit-names          Used together with --have-names for omitting the names in the file.
  --delimiter DELIMITER
                        Field delimiter for the csv file.
```
