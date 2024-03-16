#!/bin/bash
poetry build 
pip3 uninstall --break-system-packages wolfcode
pip3 install --break-system-packages .
