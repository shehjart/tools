#!/bin/sh
transposetbl  | awk '{if($0 ~ /^[a-zA-Z]/) {print "#" $0;} else {++linenum;print linenum " " $0;}}'
