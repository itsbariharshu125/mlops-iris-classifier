# DVC Workflow

## Remote Configuration

A local folder was configured as the default DVC remote:

    myremote -> ~/dvc-remote-storage

## Dataset Versioning Workflow

For each dataset change, the following workflow was used:

    dvc add
    git add
    git commit
    dvc push

## Dataset Versions

- Version 1: 150 rows
- Version 2: 170 rows

## Comparing Versions

`dvc diff` was used to compare the current dataset with a previous Git commit.

Example:

    dvc diff cf12377

This showed that `data/raw/iris_v1.csv` was modified.

## Restoring Versions

To restore Version 1:

    git checkout cf12377 -- data/raw/iris_v1.csv.dvc
    dvc checkout data/raw/iris_v1.csv.dvc

This restored 150 rows.

To restore the latest version:

    git checkout HEAD -- data/raw/iris_v1.csv.dvc
    dvc checkout data/raw/iris_v1.csv.dvc

This restored 170 rows.

## Git + DVC

Git stores the `.dvc` metadata and commit history, while DVC stores the actual dataset objects in the configured remote storage.