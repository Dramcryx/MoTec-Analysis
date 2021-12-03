import math
import csv
import copy

def float_from_string(val):
    if type(0.0) == type(val):
        return val
    else:
        return float(val.replace('"', ''))

def float_from_string(val):
    if type(0.0) == type(val):
        return val
    else:
        return float(val.replace('"', ''))

# @brief Multiplies short atomic sector
# e.g. multiply 30 mins of laps to 3 hours:
#
# \t multiply_laps(list_of_laps, 10800)
#
# Atomic means that it has all needed pitstops (tyre + fuel)
def multiply_laps(laps, untilSeconds):
    top_time = float(laps[-1][1])
    print(top_time)
    multiply_by = int(math.ceil(untilSeconds / top_time))

    laps_len = len(laps)
    
    newlaps = copy.deepcopy(laps)
    for i in range(1, multiply_by):
        newlaps += copy.deepcopy(laps)

    for i in range(1, multiply_by):
        local_top_time = top_time * i
        local_new_laps = laps_len * i
        for elem in range(laps_len * i, laps_len * (i + 1)):
            as_float = float(newlaps[elem][1])
            as_float += local_top_time
            newlaps[elem][1] = str(as_float)
            as_float = float(newlaps[elem][2])
            as_float += local_new_laps
            newlaps[elem][2] = str(as_float)

    while float(newlaps[-2][1]) > untilSeconds:
        del newlaps[-1]
    return newlaps

def multiply_laps2(laps, untilSeconds):
    top_time = float(laps[-1][1])
    print(top_time)
    multiply_by = int(math.ceil(untilSeconds / top_time))

    laps_len = len(laps)
    
    newlaps = copy.deepcopy(laps)
    for i in range(1, multiply_by):
        newlaps += copy.deepcopy(laps)

    for i in range(1, multiply_by):
        local_top_time = top_time * i
        local_new_laps = laps_len * i
        for elem in range(laps_len * i, laps_len * (i + 1)):
            as_float = float(newlaps[elem][1])
            as_float += local_top_time
            newlaps[elem][1] = str(as_float)
            as_float = float(newlaps[elem][2])
            as_float += local_new_laps
            newlaps[elem][2] = str(as_float)

    while float(newlaps[-2][1]) > untilSeconds:
        del newlaps[-1]
    return newlaps

def multiply_unreduced(laps, untilSeconds):
    top_time = float(laps[-1][1].replace('"',''))

    for i in range(len(laps) - 2, 0):
        top_time = max(top_time, float(laps[i][1].replace('"','')))
    multiply_by = int(math.ceil(untilSeconds / top_time))

    add_laps = int(laps[-1][2].replace('"','')) - int(laps[0][2])

    first_lap_end = int(laps[0][2])
    for i in range(1, len(laps)):
        if int(laps[i][2]) > first_lap_end:
            first_lap_end = i
            break
    first_lap_time = float(laps[first_lap_end - 1][1])

    laps_len = len(laps[first_lap_end:])

    #normalize fuel
    start_fuel = float(laps[0][-1])
    print(start_fuel)
    for i in laps[::-1]:
        if type(0.0) == type(i[-1]):
            as_float = float(i[-1])
            if as_float < start_fuel:
                i[-1] = start_fuel
            else:
                break
        else:
            as_float = float(i[-1].replace('"', ''))
            if as_float < start_fuel:
                i[-1] = str(start_fuel)
            else:
                break
    
    
    newlaps = copy.deepcopy(laps[first_lap_end:])
    for i in range(1, multiply_by):
        newlaps += copy.deepcopy(laps[first_lap_end:])

    for i in range(1, multiply_by):
        local_top_time = (top_time - first_lap_time) * i
        local_new_laps = add_laps * i
        for elem in range(laps_len * i, laps_len * (i + 1)):
            # print(newlaps[elem])
            as_float = 0.0
            if type(0.0) == type(newlaps[elem][1]):
                as_float = float(newlaps[elem][1])
                as_float += local_top_time
                newlaps[elem][1] = str(as_float)
                as_float = float(newlaps[elem][2])
                as_float += local_new_laps
                newlaps[elem][2] = str(as_float)
            else:
                as_float = float(newlaps[elem][1].replace('"',''))
                as_float += local_top_time
                newlaps[elem][1] = str(as_float)
                as_float = float(newlaps[elem][2].replace('"',''))
                as_float += local_new_laps
                newlaps[elem][2] = str(as_float)

    end_time_point_index = 0
    for i in range(len(newlaps) - 1, 0, -1):
        # print(float(newlaps[i][1]))
        if float(newlaps[i][1]) < untilSeconds:
            end_time_point_index = i
            break
    print('etp', end_time_point_index)
    
    last_lap = int(float(newlaps[end_time_point_index][2]))
    # print(last_lap)
    # exit(0)
    for i in range(end_time_point_index, len(newlaps)):
        if int(float(newlaps[i][2])) > last_lap:
            end_time_point_index = i
            break

    del newlaps[end_time_point_index:]
    return newlaps

def multiply_unreduced2(laps, untilSeconds):
    top_time = float(laps[-1][1])

    for i in range(len(laps) - 2, 0):
        top_time = max(top_time, float(laps[i][1]))
    multiply_by = int(math.ceil(untilSeconds / top_time))

    add_laps = int(laps[-1][2]) - int(laps[0][2])

    first_lap_end = int(laps[0][2])
    for i in range(1, len(laps)):
        if int(laps[i][2]) > first_lap_end:
            first_lap_end = i
            break
    first_lap_time = float(laps[first_lap_end - 1][1])

    laps_len = len(laps[first_lap_end:])

    #normalize fuel
    start_fuel = float(laps[first_lap_end][-1])
    print(start_fuel)
    for i in laps[::-1]:
        as_float = float(i[-1])
        if as_float < start_fuel:
            i[-1] = start_fuel
        else:
            break

    newlaps = copy.deepcopy(laps[first_lap_end:])
    for i in range(1, multiply_by):
        newlaps += copy.deepcopy(laps[first_lap_end:])

    for i in range(1, multiply_by):
        local_top_time = (top_time - first_lap_time) * i
        local_new_laps = add_laps * i
        for elem in range(laps_len * i, laps_len * (i + 1)):
            # print(newlaps[elem])
            as_float = 0.0
            
            as_float = float(newlaps[elem][1])
            as_float += local_top_time
            newlaps[elem][1] = str(as_float)
            as_float = float(newlaps[elem][2])
            as_float += local_new_laps
            newlaps[elem][2] = str(as_float)

    end_time_point_index = 0
    for i in range(len(newlaps) - 1, 0, -1):
        # print(float(newlaps[i][1]))
        if float(newlaps[i][1]) < untilSeconds:
            end_time_point_index = i
            break
    print('etp', end_time_point_index)
    
    last_lap = int(float(newlaps[end_time_point_index][2]))
    # print(last_lap)
    # exit(0)
    for i in range(end_time_point_index, len(newlaps)):
        if int(float(newlaps[i][2])) > last_lap:
            end_time_point_index = i
            break

    del newlaps[end_time_point_index:]
    return newlaps
    