#!/bin/bash
# Build packaing using osc.
set -x
set -e
echo "Building for repo $1"
if [ ! -f ./_service:recompress:tar_scm:moose-3.0.2.tar.gz ]; then
    osc service run
    osc build --noservice $1 moose-$1.spec | tee build.log
else
    osc build --noservice $1 moose-$1.spec | tee build.log
fi
