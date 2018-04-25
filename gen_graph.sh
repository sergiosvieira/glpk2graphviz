#!/bin/bash

FILE=$1
ROWS=$(cat output | grep -e "Rows:" | sed -n 's/ \+/ /gp' | cut -d " " -f 2)
COLS=$(cat output | grep -e "Columns:" | sed -n 's/ \+/ /gp' | cut -d " " -f 2)
FIRST_LINE=$((13 + ROWS))
LAST_LINE=$((FIRST_LINE + COLS - 1))
#echo "First: "$FIRST_LINE" Last: "$LAST_LINE
cat output | sed -n ${FIRST_LINE},${LAST_LINE}p | sed -n 's/ \+/ /gp' > aux
echo "digraph G {rankdir=\"LR\";"
# a -> b [ label="a to b" ];
# b -> c [ label="another label"];
while read LINE; do
	VAR=$(echo $LINE | cut -d " " -f 2);
	VAL=$(echo $LINE | cut -d " " -f 4);
	IFS='_' read -r -a array <<< $VAR
	SIZE=${#array[@]}
	c=0
	for element in "${array[@]}"; do		
		if [[ "$element" == "z1" ]]; then
			SIZE=$(( SIZE - 1 ))
			continue
		fi
		if [[ "$element" == "volGoal" ]]; then
			echo -n $element"_"${array[((c - 1))]}
		else
			if (( SIZE == 1)); then
				VAL=$VAR" = "$VAL;
			fi
			echo -n $element
		fi
		if (( c < SIZE - 1 )); then
			echo -n " -> "
		fi		
		c=$(( c + 1 ))
	done
	echo -e " [ label=\"$VAL\" ]"
done < aux
echo "}"
#cat output | sed -n 23,31p | sed -n 's/ \+/ /gp' | cut -d " " -f 3
