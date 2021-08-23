![CARROT CLI](https://github.com/broadinstitute/carrot_cli/blob/master/logo.png?raw=true)
# carrot\_cli
Command Line Interface for CARROT

Current version: 0.3.2

## Installation

    pip install .

## Development

To do development in this codebase, the python3 development package must
be installed.

After installation the carrot\_cli development environment can be set up by
the following commands:

    python3 -mvenv venv
    . venv/bin/activate
    pip install -r dev-requirements.txt
    pip install -e .

### Linting files

    # run all linting commands
    tox -e lint

    # reformat all project files
    black src tests setup.py

    # sort imports in project files
    isort -rc src tests setup.py

    # check pep8 against all project files
    flake8 src tests setup.py

    # lint python code for common errors and codestyle issues
    pylint src

### Tests

    # run all linting and test
    tox

    # run only (fast) unit tests
    tox -e unit

    # run only linting
    tox -e lint

Note: If you run into "module not found" errors when running tox for testing, verify the modules are listed in test-requirements.txt and delete the .tox folder to force tox to refresh dependencies.

### Versioning

We use `bumpversion` to maintain version numbers.
DO NOT MANUALLY EDIT ANY VERSION NUMBERS.

Our versions are specified by a 3 number semantic version system (https://semver.org/):

	major.minor.patch

To update the version with bumpversion do the following:

`bumpversion PART` where PART is one of:
- major
- minor
- patch

This will increase the corresponding version number by 1.
