#!/bin/sh
nosetests --cover-package=wooper --with-coverage &&
python -m coverage html
