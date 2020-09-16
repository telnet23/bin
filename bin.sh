#!/bin/bash

BIN="$HOME/.local/bin"
mkdir -p "$BIN"

find "$@" -maxdepth 1 -not -type d -executable | while read src
do
    bn="$(basename "$src")"
    dst="$BIN/.${bn%.*}"

    if [ ! -e "$dst" ]
    then
        ln -rs "$src" "$dst"
    fi
done
