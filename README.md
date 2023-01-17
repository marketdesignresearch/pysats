# PySATS

This is a bridge to use some features of [SATS](https://spectrumauctions.org/) in a Python project.

## Requirements

- Python: 3.8+ (required for guaranteeing insertion order in dicts)
- Pyjnius 1.3.0

## Set up

1. Create a Python environment that satisfied above requirements. To install Pyjnius, follow the steps in <https://pyjnius.readthedocs.io/en/stable/installation.html>#.
2. Download the latest SATS JAR from <https://github.com/spectrumauctions/sats/releases/>
3. Place the SATS JAR together with the cplex.jar (which can be found in the CPLEX installation's `bin` folder) together in some directory on your machine, and set the PYJNIUS_CLASSPATH environment variable to the absolute path of this directory.

## Usage

After having set up the environment according the the previous section, install the package

```bash
$ pip install pysats
...
```

Use it in your project as follows. Have a look at the `test/` directory for more examples.

```python
from pysats import PySats

gsvm = PySats.getInstance().create_gsvm()
for bidder_id in gsvm.get_bidder_ids():
    goods_of_interest = gsvm.get_goods_of_interest(bidder_id)
    print(f'Bidder_{bidder_id}: {goods_of_interest}')
```

## Verify installation

The best way to verify installation, and check if everything is wired up correctly, is to check out the project and to run the tests:

```bash
$ python -m unittest
...
```

### Alternative to set up locally: Poetry

You can use Poetry to set up and test pysats locally. Install it as described in <https://python-poetry.org/docs/#installation>, and then run:

```bash
$ poetry install
...
```

This will install all dependencies automatically. To test the setup, run:

```bash
$ poetry run python -m unittest
...
```
