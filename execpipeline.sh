#!/bin/bash

input=$1
cutby=$2
hours=$3
preprocessdir=$4
storageHost=$5

if [ -d $preprocessdir ]
then
    rm -rf $preprocessdir/
fi

mkdir $preprocessdir

echo "args - $@"

./preprocessor --cut=$cutby --hours=$hours --file=$input --output=$preprocessdir

spark-submit --master=local[2] ./spark.py --file=$preprocessdir/outdata.csv --output=$preprocessdir --hours=$hours --cut=$cutby

mv $(find $preprocessdir/spark/ -iname "*.csv") $preprocessdir/outdata_final.csv
rm -rf $preprocessdir/spark/

./clickhouse-loader --file=$preprocessdir --host=$storageHost