#!/usr/bin/env bash

coverage run --source . ./manage.py test && coverage report
