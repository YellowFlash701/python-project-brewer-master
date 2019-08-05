#!/bin/bash
rm dist/*
python setup.py sdist bdist_wheel
rm dist/*.egg
twine upload dist/*


# [ai:2026-07-23] # Use double quotes for PYPI username env var
