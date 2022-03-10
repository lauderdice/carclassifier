#!/bin/sh
gunicorn main:application -w 1 -b 0.0.0.0:8888