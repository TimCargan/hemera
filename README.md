# Hemera

A collection of my personal scripts and library functions common to many of my projects.

## Libaray
- `hemra.standard_logger` - pretty prints absl.logging calls and adds slurm info
- `hemra.path_translator` - A standard, config driven, way to get paths for files when working on multiple hosts

### Install

Easy installation with:
```shell
pip install git@https://github.com/timcargan/hemera.git
```

to install an editable version run:

```shell
git clone https://github.com/timcargan/hemera.git
cd hemera
pip install -e .
```

## Scripts
Basic slurm bash scripts to do some things. Its nice to put them on the $PATH for easy use.

- `scripts/spython` - A way to run python scripts in the slurm context, extracts a string of `SBATCH` params. Sample usage:

  ```shell
  spython ["--slurm opts"] script.py [args]
  ```