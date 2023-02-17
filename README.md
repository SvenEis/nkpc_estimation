# The New Keynesian Phillips Curve: An Empirical Assessment

[![image](https://img.shields.io/github/actions/workflow/status/SvenEis/nkpc_estimation/main.yml?branch=main)](https://github.com/SvenEis/nkpc_estimation/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/SvenEis/nkpc_estimation/branch/main/graph/badge.svg)](https://codecov.io/gh/SvenEis/nkpc_estimation)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/SvenEis/nkpc_estimation/main.svg)](https://results.pre-commit.ci/latest/github/SvenEis/nkpc_estimation/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Repo Size](https://img.shields.io/github/repo-size/SvenEis/nkpc_estimation)

## Repository Information

This is the repository to the final project for the course *Effective programming
practices for economists* by [Sven Eis](https://sveneis.github.io). It contains all
necessary scripts to reproduce the dependencies of the paper, and to compile the paper
itself.

## Usage

### Environment

To reproduce this repository you need to install the required packages with the package
manager conda ([Installation](https://docs.conda.io/en/latest/miniconda.html)). Once
installed, open a shell and execute the following:

```console
$ cd /to/project/root
$ conda env create -f environment.yml
$ conda activate nkpc_estimation
```

### pytask

Once the environment is installed and activated, build the project by executing

```console
$ pytask
```

The [`pytask`](https://github.com/pytask-dev/pytask) command executes all necessary
scripts.

### Results

After running `pytask`, a new folder named `bld` is created with all the files.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
