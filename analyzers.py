def get_fuel_pitstops(lapscatters, fuel_index, lapindex):
    fuelpitstops = []
    asc = False
    fuel_this_line = float(lapscatters[0][fuel_index])
    for lap in lapscatters[1:]:
        fuel_last_line = 0.0
        fuel_last_line = lap[fuel_index]
        if fuel_this_line > fuel_last_line and not asc:
            asc = True
            fuelpitstops.append([lap[0], lap[lapindex]])
        elif fuel_this_line < fuel_last_line:
            asc = False
        fuel_this_line = fuel_last_line
    return fuelpitstops

def get_tyre_pitstops(lapscatters, tyre_index, lapindex):    
    tyre_pitsops = []
    asc = False
    tyre_this_line = float(lapscatters[0][tyre_index])
    for lap in lapscatters[1:]:
        tyre_last_line = 0.0
        if type(0.0) == type(lap[tyre_index]):
            tyre_last_line = lap[tyre_index]
        else:
            tyre_last_line = float(lap[tyre_index].replace('"', ''))
        if tyre_this_line > tyre_last_line and not asc:
            asc = True
            tyre_pitsops.append([lap[0], lap[lapindex]])
        elif tyre_this_line < tyre_last_line:
            asc = False
        tyre_this_line = tyre_last_line
    return tyre_pitsops


def get_laps(lapscatters, indexoflap, field_reduction_rules, remove_laps):
    laps = []
    current_lap_scatter = 0

    for scatter in range(1, len(lapscatters)):
        if lapscatters[scatter][indexoflap] == lapscatters[current_lap_scatter][indexoflap]:
            continue
        laprange = range(current_lap_scatter, scatter)
        lapdata = [0.0] * len(lapscatters[scatter])
        
        for lap in laprange:
            for j in range(len(lapscatters[lap])):
                lapscatters[lap][j] = float(lapscatters[lap][j].replace('"',''))
            lapscatters[lap][indexoflap] = int(lapscatters[lap][indexoflap]) - remove_laps + 1
        for index in range(len(lapdata)):
            lapdata[index] = field_reduction_rules[index](lapscatters, index, laprange)
        laps.append(lapdata)
        current_lap_scatter = scatter
    
    laprange = range(current_lap_scatter, len(lapscatters))
    lapdata = [0.0] * len(lapscatters[-1])
    
    for lap in laprange:
        for j in range(len(lapscatters[lap])):
            lapscatters[lap][j] = float(lapscatters[lap][j].replace('"',''))
        lapscatters[lap][indexoflap] = int(lapscatters[lap][indexoflap]) - remove_laps + 1
    for index in range(len(lapdata)):
        lapdata[index] = field_reduction_rules[index](lapscatters, index, laprange)
    laps.append(lapdata)
    return laps