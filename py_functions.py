get_ipython().run_line_magic('matplotlib', 'notebook')
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt


# **functions**

# useful function to quickly get derive datetime (string)
def get_datetime(pre_midnight, hour, minutes, seconds=0, as_string=False):
    date = "18/06/2020" if pre_midnight else "19/06/2020"
    time = str(hour).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
    date_str = date + " " + time
    if as_string:
        return date_str
    else:
        return datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')

def str_to_datetime(datetime_str):
    #TODO str from ind
    return datetime.datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')

# make boxcar --> for plot
def get_boxcars(state_onsets, depths_succ):
    boxcar_times  = []
    boxcar_depths = []
    for i in range(len(state_onsets)):
        current_time = state_onsets[i]
        last_state   = depths_succ[i - 1] if i > 0 else 0
        boxcar_times.append(current_time)
        boxcar_times.append(state_onsets[i])
        boxcar_depths.append(last_state)
        boxcar_depths.append(depths_succ[i])
    # make it look nicer: show last (final) wake stage (--> daytime)
    boxcar_times.append(state_onsets[-1])
    boxcar_depths.append(0)
    # already convert datetimes to plt numbers at this point (since this function is only important for plotting anyway)
    dates = matplotlib.dates.date2num(boxcar_times)
    return [dates, boxcar_depths]

def get_ax(state_onsets, depths_succ):
    fig, ax = plt.subplots(figsize=(10,4))
    bc = get_boxcars(state_onsets, depths_succ)
    ax.plot_date(bc[0], bc[1], xdate=True, linestyle='solid', marker='None', linewidth=3)
    #ax.plot_date(state_onsets, depths_succ, xdate=True, linestyle='solid', marker='None')
    fmt = matplotlib.dates.DateFormatter('%H:%M:%S')
    plt.gca().xaxis.set_major_formatter(fmt)
    ax.set_yticks(list(sleep_depths.values()))    
    ax.set_yticklabels(list(sleep_depths.keys()))
    return ax

# dictionary to translate strings to sleep depths
sleep_depths = {
    "Wach":             0,
    "Leichter Schlaf": -1,
    "Tiefschlaf":      -2
}

def read_raw_data(df):
    # get the two important columns: indices 1, 3, 4
    stage_succ = df.iloc[:,[1,3,4]]
    stage_succ

    # add the last "beenden" time (column ind 1) to "beginn" (column ind 0)
    # then "beenden" column is completely redundant and can be removed
    last_stage_end = stage_succ.iloc[-1,1]
    last_stage     = stage_succ.iloc[-1,2]

    state_onsets_str = stage_succ.iloc[:,0].to_list() + [last_stage_end]
    state_labels    = stage_succ.iloc[:,2].to_list() + [last_stage]
    state_onsets = [str_to_datetime(s) for s in state_onsets_str]
    depths_succ  = [sleep_depths[s]    for s in state_labels]
    
    return [state_onsets, depths_succ]