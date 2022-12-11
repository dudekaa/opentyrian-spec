#!/bin/bash
#
# Used to upload packages to COPR [ and that triggers build ]
#

set -eu

LOCAL_BUILD=""

function log {
   echo "BUILD.SH | $(date +"%Y/%m/%d %H:%M:%S") | $@"
}

function help {
    echo ""
    echo "Usage: ./build.sh [-h] [-l]"
    echo ""
    echo "Options:"
    echo "-h        show help"
    echo "-l        builds localy"
}

while getopts ":hl" opt; do
    case ${opt} in
        h ) # process option h
        help
        exit 0
        ;;
        l ) # process option l
        LOCAL_BUILD="1"
        ;;
        \? )
        echo "Unknown option: $OPTARG" 1>&2
        help
        exit 1
        ;;
    esac
done

# exit when uncommited changes are present
if ! git diff-index --quiet HEAD --; then
    log "Uncomitted changes detected. Aborting..." 1>&2
    exit 1
fi

# run linter on spec
log "Running linter..."
rpkg lint

if [ -n "$LOCAL_BUILD" ]; then
    log "Trying to build locally..."
    rpkg compile
else
    log "Tagging release..."
    rpkg tag

    log "Building in COPR..."
    #copr-cli build opentyrian "$PACKAGE"
    rpkg build -w nost23/opentyrian
fi

# vim: set ff=unix expandtab ts=4:
