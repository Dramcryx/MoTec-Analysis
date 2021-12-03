import csv
import json
import uuid
import argparse

import util.analyzers as analyzers
import util.reducers as reducers
import util.multiplier as multiplier

parser = argparse.ArgumentParser(description='Process data')
parser.add_argument('--cut', type=int, help='Where to cut broken tail stats')
parser.add_argument('--hours', type=int, help='To how many hours multiply the data')
parser.add_argument('--file', type=str, help='Input data')
parser.add_argument('--output', type=str, help='Output path')

args = parser.parse_args()
metadatajson = json.loads('{}')

file = args.file
#['"Time"', '"Lap Number"', '"Max Straight Speed"', '"Min Corner Speed"', '"Ground Speed"', '"Tyre Wear FL"', '"Tyre Wear FR"', '"Tyre Wear RL"', '"Tyre Wear RR"', '"Fuel Level"']
indexoftime = 0
indexoflap = 1
indexofmaxstraightspeed = 2
indexofmincornerspeed = 3
indexofgroundspeed = 4
indexoffl = 5
indexoffr = 6
indexofrl = 7
indexofrr = 8
indexoffuel = 9
workaround = [None] * 10
raceid = str(uuid.uuid4())

def fill_driver(strlist):
    metadatajson['driver'] = strlist[1].replace('"','')

def fill_track(strlist):
    metadatajson['track'] = strlist[1].replace('"','')

def fill_vehicle(strlist):
    metadatajson['vehicle-class'] = strlist[1].replace('"','')
    metadatajson['vehicle-name'] = strlist[5].replace('"','')

def fill_date(strlist):
    metadatajson['date'] = strlist[1].replace('"','')

def fill_time(strlist):
    metadatajson['time'] = strlist[1].replace('"','')

def fill_rate(strlist):
    metadatajson['samples-per-sec'] = strlist[1].replace('"','')

def fill_duration(strlist):
    metadatajson['duration-seconds'] = strlist[1].replace('"','')

def get_metadata(csvreader: csv.reader):
    expected_fields = {
        '"Driver"': fill_driver,
        '"Venue"': fill_track,
        '"Vehicle"': fill_vehicle,
        '"Log Date"': fill_date,
        '"Log Time"': fill_time,
        '"Sample Rate"': fill_rate,
        '"Duration"' : fill_duration
    }
    for row in csvreader:
        if len(row) == 0 or not row[0] in expected_fields:
            continue
        expected_fields[row[0]](row)
        expected_fields.pop(row[0])
        if len(expected_fields) == 0:
            break
    if len(expected_fields) != 0:
        raise LookupError("Not all objects were found in CSV!")

globalfields = []

def get_fields(csvreader: csv.reader):
    row_fields      = []
    row_field_types = []
    expected_fields = ['"Time"', '"Lap Number"', '"Max Straight Speed"', '"Min Corner Speed"', '"Ground Speed"', '"Tyre Wear FL"', '"Tyre Wear FR"', '"Tyre Wear RL"', '"Tyre Wear RR"', '"Fuel Level"']
    expected_field_types = ['"s"', '""', '"km/h"', '"km/h"', '"km/h"', '"%"', '"%"', '"%"', '"%"', '"l"']
    for row in csvreader:
        if len(row) == 0:
            continue
        if row[0] in expected_fields:
            row_fields = row
            continue
        if row[0] in expected_field_types:
            row_field_types = row
            continue
        if len(row_fields) != 0 and len(row_field_types) != 0:
            break
    fields = {"id": ""}
    for i in range(len(row_fields)):
        fields[row_fields[i].replace('"','')] = row_field_types[i].replace('"','')
    workaround[indexoflap] = row_fields.index('"Lap Number"')
    workaround[indexoftime] = row_fields.index('"Time"')
    workaround[indexofmaxstraightspeed] = row_fields.index('"Max Straight Speed"')
    workaround[indexofmincornerspeed] = row_fields.index('"Min Corner Speed"')
    workaround[indexofgroundspeed] = row_fields.index('"Ground Speed"')
    workaround[indexoffl] = row_fields.index('"Tyre Wear FL"')
    workaround[indexoffr] = row_fields.index('"Tyre Wear FR"')
    workaround[indexofrl] = row_fields.index('"Tyre Wear RL"')
    workaround[indexofrr] = row_fields.index('"Tyre Wear RR"')
    workaround[indexoffuel] = row_fields.index('"Fuel Level"')
    global globalfields
    globalfields = [i.replace('"','').replace(' ','') for i in expected_fields]
    metadatajson['fields'] = fields

lap = 0
with open(file, newline='') as csvfile:
    counter = 0
    moteccsv = csv.reader(csvfile, delimiter=',', quotechar='|')
    get_metadata(moteccsv)
    get_fields(moteccsv)

    lines = []
    firstrow = moteccsv.__next__()
    lap = int(firstrow[indexoflap].replace('"', ''))

    for row in moteccsv:
        if len(row) == 0:
            continue
        if int(row[indexoflap].replace('"', '')) == args.cut:
            break
        if '""' in row:
            continue
        lines.append(row)

reductionRules = {
    indexoffuel: reducers.maxVal,
    indexoffl: reducers.maxVal,
    indexoffr: reducers.maxVal,
    indexofrl: reducers.maxVal,
    indexofrr: reducers.maxVal,
    indexofmaxstraightspeed: reducers.maxVal,
    indexofgroundspeed: reducers.avgVal,
    indexofmincornerspeed: reducers.minVal,
    indexoftime: reducers.maxVal,
    indexoflap: reducers.firstVal
}

laps = analyzers.get_laps(lines, workaround[indexoflap], reductionRules, lap)
laps = multiplier.multiply_laps2(laps, 3600 * args.hours)
for i in laps:
    i.insert(0, raceid)

laptimes = []
prev_time = 0.0
for i in laps:
    laptime = float(i[1]) - prev_time
    laptimes.append([i[2], laptime])
    prev_time = float(i[1])

with open(args.output+'/metadata.json', 'w', newline='') as metadatafile:
    metadatajson['UUID'] = raceid
    metadatajson['config-name'] = args.output.replace('."', '')
    metadatafile.write(json.dumps(metadatajson, indent=4))
    print(json.dumps(metadatajson, indent=4))

with open(args.output+'/laptimes.csv', 'w', newline='') as csvfile:
    outcsv = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for t in laptimes:
        t.insert(0, raceid)
        outcsv.writerow(t)
        print(t)

with open(args.output+'/outdata.csv', 'w', newline='') as csvfile:
    outcsv = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    globalfields.insert(0, "ID")
    outcsv.writerow(globalfields)
    for row in lines:
        row.insert(0, raceid)
        outcsv.writerow(row)
with open(args.output+'/outdata_reduced_by_laps.csv', 'w', newline='') as csvfile:
    outcsv = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in laps:
        outcsv.writerow(row)

# more_laps = multiplier.multiply_unreduced2(lines, 3600 * args.hours)

# fuelpitstops = analyzers.get_fuel_pitstops(more_laps, workaround[indexoffuel] + 1, workaround[indexoflap] + 1)
# tyrepitstops = analyzers.get_fuel_pitstops(more_laps, workaround[indexoffl] + 1, workaround[indexoflap] + 1)

# with open('fuelpits.csv', 'w', newline='') as csvfile:
#     outcsv = csv.writer(csvfile, delimiter=',',
#                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     outcsv.writerows(fuelpitstops)

# with open('tyrepits.csv', 'w', newline='') as csvfile:
#     outcsv = csv.writer(csvfile, delimiter=',',
#                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     outcsv.writerows(tyrepitstops)


# with open('outdata_multiplied.csv', 'w', newline='') as csvfile:
#     outcsv = csv.writer(csvfile, delimiter=',',
#                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     outcsv.writerows(more_laps)
