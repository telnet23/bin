#!/bin/bash

while inotifywait -re attrib,create,delete,modify,move "$1/"
do
    rsync -a --progress --verbose "$1/" "$2:$1/"
done
