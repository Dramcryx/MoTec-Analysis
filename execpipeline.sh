#!/bin/bash

input=$1
cutby=$2
hours=$3
preprocessdir=$4

rf -rf $preprocessdir

mkdir $preprocessdir

echo "args - $@"

python ./main2.py --cut=$cutby --hours=$hours --file=$input --output=$preprocessdir

~/.local/bin/spark-submit --master=local[2] ./spark.py --file=$preprocessdir/outdata.csv --output=$preprocessdir --hours=$hours --cut=$cutby

mv $(find $preprocessdir/spark/ -iname "*.csv") $preprocessdir/outdata_final.csv

python ./clickhouse-loader.py --file=$preprocessdir