#!/bin/bash

FILE=$1

glpsol --lp --nopresol -o output $FILE; ./gen_graph.py output | pbcopy 

