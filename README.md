# dafact
Encodes data as ASP facts.

```dafact``` solves the reiterative task of encoding a dataset into a set of Answer Set Programming facts. The resulting ASP program, which can be partially personalized, can be encoded as [python clingo](https://github.com/potassco/clingo) objects directly or as plain text, and it handles floating point numbers automatically.

Data can be fed into ```dafact``` through CSV files, [numpy](https://github.com/numpy/numpy) arrays, [pandas](https://github.com/pandas-dev/pandas) DataFrames and other typical formats.

It can be used both as a python library and as a command line tool.

# Installation
The tool is easily installable through ```pip```:
```
python3 -m pip install dafact
```

## Short usage

[A more detailed usage guide can be found here](examples/README.md).

### Python
```Dafacter``` python class provides all the funcionality. Once fed with data, a ```Dafacter``` object provides two main methods for obtaining a logic program:
```python
from dafact import Dafacter
dafacter = Dafacter("data/haberman.csv", have_names=True) # Fed data into the object
clingo_facts = dafacter.as_clingo_facts()  # Returns a list of clingo.Function objects
program_text = dafacter.as_program_string()  # Returns the program as plain text
```

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

The encoded style can also be tweaked easily, and it accepts different kind of data sources from [numpy](https://github.com/numpy/numpy) arrays to [pandas](https://github.com/pandas-dev/pandas) DataFrames. A more detailed guide on usage of the python library can be found in [examples folder](examples/README.md).

### Command line tool
Once installed through ```pip``` users can use ```dafact``` for directly obtain a logic program from csv files through the use of the **command line tool**. The usage of the tool is the same to the use of the ```Dafacter``` python class for csv files.

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

