import argparse
import math

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.window import Window
import pyspark.sql.functions as f
# from pyspark.sql.functions import col,array_contain

def setFuel(row, fuel, lap):
    ret = [i for i in row]
    if row[2] == lap and row[-1] > fuel:
        ret[-1] = fuel
    return ret

def addToTel(row, time, lap):
    ret = [i for i in row]
    ret[1] += time
    ret[2] += lap
    return ret

parser = argparse.ArgumentParser(description='Process data')
parser.add_argument('--cut', type=int, help='Where to cut broken tail stats')
parser.add_argument('--hours', type=int, help='To how many hours multiply the data')
parser.add_argument('--file', type=str, help='Input data')
parser.add_argument('--output', type=str, help='Input data')

args = parser.parse_args()

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

struct = StructType() \
    .add('ID', StringType(), False) \
    .add('Time', DoubleType(), False) \
    .add('LapNumber', IntegerType(), False) \
    .add('MaxStraightSpeed', DoubleType(), False) \
    .add('MinCornerSpeed', DoubleType(), False) \
    .add('GroundSpeed', DoubleType(), False) \
    .add('TyreWearFL', DoubleType(), False) \
    .add('TyreWearFR', DoubleType(), False) \
    .add('TyreWearRL', DoubleType(), False) \
    .add('TyreWearRR', DoubleType(), False) \
    .add('FuelLevel', DoubleType(), False)

tel = spark.read.csv(args.file, header=True, schema=struct)
tel = tel.filter(tel.LapNumber < args.cut)

# step 1: pick needed stuff
maxTime = tel.groupBy().agg(f.max("Time")).collect()[0][0]
maxLap = tel.groupBy().agg(f.max("LapNumber")).collect()[0][0]
minLap = tel.groupBy().agg(f.min("LapNumber")).collect()[0][0]
addLaps = maxLap - minLap
firstLap = tel.first()
secondLap = tel.filter(tel.LapNumber > firstLap[2]).take(1)
lastFuel = secondLap[0][-1]

lapsToFix = tel.filter(tel.FuelLevel > lastFuel).orderBy(f.desc("LapNumber"))
lastLapToFix = lapsToFix.take(1)[0][2]

etalonWithFirstLap = tel.rdd.map(lambda row: setFuel(row, lastFuel, lastLapToFix)).toDF(schema=struct)
etalonWithoutFirstLap = etalonWithFirstLap.filter(etalonWithFirstLap.LapNumber > firstLap[2])

multiplyBy = int(math.ceil(args.hours * 3600 / maxTime))
# cutExcessive = lapAtHour + (lapAtHour - firstLap[2]) * (args.hours - 1)

replicas = []

avgLapTime = maxTime / addLaps

maxSeconds = args.hours * 3600 + avgLapTime

for i in range(1, multiplyBy):
    iTel = etalonWithoutFirstLap.alias(str(i) + 'Tel')
    replicas.append(iTel.rdd.map(lambda row: addToTel(row, maxTime * i, addLaps * i)).toDF(schema=struct))

sourceTel = tel.alias('sourceTel')
for i in replicas:
    sourceTel = sourceTel.union(i)

sourceTel = sourceTel.filter(sourceTel.Time < maxSeconds)
lastLap = sourceTel.groupBy().agg(f.max("LapNumber")).collect()[0][0]
sourceTel = sourceTel.filter(sourceTel.LapNumber < lastLap)

sourceTel.coalesce(1).write.format("csv").option("header", False).save(args.output + "/spark")
