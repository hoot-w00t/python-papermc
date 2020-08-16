# python-papermc
![License](https://img.shields.io/github/license/hoot-w00t/python-papermc?style=flat-square) ![Python Version](https://img.shields.io/pypi/pyversions/python-papermc?style=flat-square) [![PyPI](https://img.shields.io/pypi/v/python-papermc?style=flat-square)](https://pypi.org/project/python-papermc/)

Python wrapper for the PaperMC Downloads API (https://papermc.io)

## Installing
Using PyPI:
```
python3 -m pip install python-papermc
```

## Example usage
```py
import papermc

with papermc.Paper() as paper:
    version = paper.get_latest_version()
    paper.download_build_to_file("paper-{}.jar".format(version), version, "latest")
```

## How to use
- `Paper()`, `Waterfall()` and `Travertine()` provide the following functions:
    - `get_versions()`
      - Returns a `list` of available versions
    - `get_latest_version()`
      - Returns the latest version
    - `get_builds(version)`
      - Returns a `list` of builds for `version`
    - `get_latest_build(version)`
      - Returns the latest build for `version`
    - `download_build(version, build)`
      - Both `version` and `build` can be set to `latest`
      - Returns the corresponding JAR file's `bytes`
    - `download_build_to_file(filepath, version, build)`
      - Same as above but writes the JAR file's bytes to `filepath` instead of returning them

- `get_from_name(project_name)`
  - Returns the corresponding class from the project name (e.g. `paper` will return a `Paper()` object)
  - Raises a `ProjectNotFoundError` if the project name is invalid