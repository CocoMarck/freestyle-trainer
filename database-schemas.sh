#!/bin/bash
dir="$(dirname "$(realpath "$0")")"

cat $dir"/schemas/stimulus_generator/"*.sql > $dir"/docs/database-schemas.txt"
