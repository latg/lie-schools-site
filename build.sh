#!/bin/sh
set -eu

if [ -z "${HUGO_PARAMS_PHOTOBASEURL:-}" ]; then
    exec hugo --destination public
fi

photo_static_dir=$(mktemp -d)
trap 'rm -rf "$photo_static_dir"' EXIT

# Filter static assets before Hugo renders gallery HTML, including 2018/photo/.
rsync -a --exclude='[Pp]hoto/' --exclude='[Pp]hotos/' \
    --exclude='[Pp]reviews/' --exclude='Everyone.jpg' static/ "$photo_static_dir/"

# Clean stale local photos when switching an existing output to external mode.
HUGO_STATICDIR="$photo_static_dir" hugo --destination public --cleanDestinationDir
