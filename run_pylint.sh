#!/bin/bash
export PYTHONPATH=/c/pythonworkspace/ojrtennis
pylint --extension-pkg-whitelist=pygame  --rcfile=.pylintrc ../ojrtennis
