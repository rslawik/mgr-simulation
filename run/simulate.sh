#!/bin/sh
GENERATE="../generate.py"
SIMULATE="../simulate.py"
THROUGHPUT="../throughput.py"

if [ $# -lt 4 ]
then
	echo "$0 <generator> <n> <alg> <adv>"
	exit
fi

MODEL="model.in"
GENERATOR=$1
N=$2
ALG=$3
ADV=$4

i=1
while [ $i -le 5 ]
do
	echo $i

	# generate
	$GENERATE $GENERATOR $N $MODEL > $i.in

	# simulate
	$SIMULATE $ALG $ADV $i.in $MODEL > $i.log

	# throughput
	$THROUGHPUT $i.log >> out

	i=`expr $i + 1`
done

sed 's/\./,/' out | awk '{ total += $1; count++ } END { print total/count }'
