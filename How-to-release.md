# Release

Change version number in `awstool/__init__.py`

## Install `twine` and `wheel`

```shell script
pip install twine wheel
```

## Configure `twine`

The contents of `.pypirc` file can be seen below.
This file must be placed in `~/.pypirc` for pip/twine to use it.

```shell script
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username: zhan9san
password: xxx

[pypitest]
repository: https://test.pypi.org/legacy/
username: zhan9san
password: xxx
```

## Using `twine`

1. Create some distributions in the normal way:

    ```shell script
    python setup.py sdist bdist_wheel
    ```

2. Upload with `twine` to Test PyPI and verify things look right.
Twine will automatically prompt for your username and password:

    ```shell script
    twine upload -r testpypi dist/*
    ```

3. Upload to PyPI:

    ```shell script
    twine upload dist/*
    ```
