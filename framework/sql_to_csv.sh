#!/bin/bash

tmpdir="$(mktemp -d)"
tmpfifo="$tmpdir/fifo"
mkfifo "$tmpfifo"
echo "$tmpfifo"

# Export result of query to fifo
cat | mysql --batch --raw $@ > "$tmpfifo"

rm "$tmpfifo"
rmdir "$tmpdir"
