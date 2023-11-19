#!/bin/bash
#

set -ue

FILENAME="opentyrian.spec"

rpmdev-bumpspec -r "$FILENAME"
