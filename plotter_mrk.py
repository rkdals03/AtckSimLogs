# input: file to read(e.g. sensor_accel_0), folders to read from
# e.g. python3 plotter.py sensor_accel_0 -a 230925_atck -b 230925_vanilla
# flags: -a --attack: attacked log folder to read from
#        -b --benign: benign   log folder to read from
# plot using matplotlib and seaborn library
# output:   plot of the data, time-value graph
#           green for benign, red for attacked
#           saved as png file
#           plot title: sensor_accel_0 -a 230925_atck -b 230925_vanilla
#           plot name:  sensor_accel_0-230925_atck-230925_vanilla.png

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import os

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to read")
parser.add_argument("-a", "--attack", help="attack folder to read from")
parser.add_argument("-b", "--benign", help="benign folder to read from")
parser.add_argument("-m","--marker", action='store_true', help="commander takeoff같이 명령어가 들어간 순간에 vertical dotted line indicator 추가 및 설명 추가 필요")
# parser.add_arguemtn("-r","--range", nargs = 4 ,type = float, help="[x-min, x-max, y-min, y-max] x,y, area setting")
args = parser.parse_args()

# AREA: read attacked data
# first, find the attacked log file from attack folder. find a file thats name contains the args.file string
# get a list of all files in the directory
files = os.listdir(args.attack)

# loop through the list to find the file that contains the args.file string value
atk_file = None
for file in files:
    if args.file in file:
        atk_file = file
        break

if atk_file is None:
    print(f"No log file found in {args.attack} directory that contains {args.file} string.")
    exit()
else:
    print(f"Found attack log file: {atk_file}")

# now read from the log file
pd_atk = pd.read_csv(os.path.join(args.attack, atk_file))
print(pd_atk.head())

# AREA: read benign data
# then, find the benign log file from benign folder. find a file thats name contains the args.file string    import os
# get a list of all files in the directory
files = os.listdir(args.benign)

# loop through the list to find the file that contains the args.file string value
ben_file = None
for file in files:
    if args.file in file:
        ben_file = file
        break

if ben_file is None:
    print(f"No log file found in {args.benign} directory that contains {args.file} string.")
    exit()
else:
    print(f"Found benign log file: {ben_file}")

# now read from the log file
pd_ben = pd.read_csv(os.path.join(args.benign, ben_file))
print(pd_ben.head())

if args.marker == True:
    for file in files:
        if "command" in file:
            mrk_file = file
            break
    pd_mrk = pd.read_csv(os.path.join(args.benign, mrk_file))
    print(pd_mrk)

# AREA: merge data
# reset timestamp to start from 0
# pd_atk['timestamp'] = pd_atk['timestamp'] - pd_atk['timestamp'][0]
# pd_ben['timestamp'] = pd_ben['timestamp'] - pd_ben['timestamp'][0]
pd_atk['timestamp'] = pd_atk['timestamp'] - 0
pd_ben['timestamp'] = pd_ben['timestamp'] - 0
if args.marker == True:
    pd_mrk['timestamp'] = pd_mrk['timestamp'] - 0

# merge the two dataframes, after changing the column names
# atk: x,y,z > atk_x, atk_y, atk_z | ben: x,y,z > ben_x, ben_y, ben_z
pd_merged = pd.DataFrame()
pd_merged['timestamp'] = pd_atk['timestamp']/1000000
pd_merged['atk_x'] = pd_atk['x']
pd_merged['atk_y'] = pd_atk['y']
pd_merged['atk_z'] = pd_atk['z']
pd_merged['ben_x'] = pd_ben['x']
pd_merged['ben_y'] = pd_ben['y']
pd_merged['ben_z'] = pd_ben['z']
if args.marker == True:
    pd_merged['mrk'] = pd_mrk['timestamp']/1000000
print(pd_merged)

# AREA: plot

plt.figure(figsize=(20, 10))
plt.title(f"{args.file} -a {args.attack} -b {args.benign}")
plt.plot(pd_merged['timestamp'], pd_merged['atk_x'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_x'], color='green', label='benign')
# edit: show only 3 std range of data
plt.ylim(pd_merged['atk_x'].mean() - 3 * pd_merged['atk_x'].std(), pd_merged['atk_x'].mean() + 3 * pd_merged['atk_x'].std())
# plt.xlim(0,60)
plt.legend(loc='upper right')
plt.xlabel('time [s]')
plt.ylabel('accel_x [m/s^2]')
# plot vertical lines at 20,30,50,60,80,90
plt.axvline(x=20, color='black', linestyle='--')
plt.axvline(x=30, color='black', linestyle='--')
plt.axvline(x=50, color='black', linestyle='--')
plt.axvline(x=60, color='black', linestyle='--')
plt.axvline(x=60+20, color='black', linestyle='--')
plt.axvline(x=60+30, color='black', linestyle='--')
plt.axvline(x=60+50, color='black', linestyle='--')
plt.axvline(x=60+60, color='black', linestyle='--')
plt.axvline(x=120+20, color='black', linestyle='--')
plt.axvline(x=120+30, color='black', linestyle='--')
if args.marker == True:
    ymin = pd_merged['atk_x'].mean() - 3 * pd_merged['atk_x'].std()
    ymax = pd_merged['atk_x'].mean() + 3 * pd_merged['atk_x'].std()
    plt.vlines(x=pd_merged['mrk'], ymin=ymin, ymax = ymax, color='blue', linestyles='dotted')
# plt.axvline(x=80, color='black', linestyle='--')
# plt.axvline(x=90, color='black', linestyle='--')
plt.savefig(f"{args.file}-{args.attack[2:]}-{args.benign[2:]}_x.png")

plt.figure(figsize=(20, 10))
plt.title(f"{args.file} -a {args.attack} -b {args.benign}")
plt.plot(pd_merged['timestamp'], pd_merged['atk_y'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_y'], color='green', label='benign')
# edit: show only 3 std range of data
plt.ylim(pd_merged['atk_y'].mean() - 5 * pd_merged['atk_y'].std(), pd_merged['atk_y'].mean() + 5 * pd_merged['atk_y'].std())
# plt.xlim(0,60)
plt.axvline(x=20, color='black', linestyle='--')
plt.axvline(x=30, color='black', linestyle='--')
plt.axvline(x=50, color='black', linestyle='--')
plt.axvline(x=60, color='black', linestyle='--')
plt.axvline(x=60+20, color='black', linestyle='--')
plt.axvline(x=60+30, color='black', linestyle='--')
plt.axvline(x=60+50, color='black', linestyle='--')
plt.axvline(x=60+60, color='black', linestyle='--')
plt.axvline(x=120+20, color='black', linestyle='--')
plt.axvline(x=120+30, color='black', linestyle='--')
if args.marker == True:
    ymin = pd_merged['atk_x'].mean() - 3 * pd_merged['atk_x'].std()
    ymax = pd_merged['atk_x'].mean() + 3 * pd_merged['atk_x'].std()
    plt.vlines(x=pd_merged['mrk'], ymin=ymin, ymax = ymax, color='blue', linestyles='dotted')
plt.legend(loc='upper right')
plt.xlabel('time [s]')
plt.ylabel('accel_y [m/s^2]')
plt.savefig(f"{args.file}-{args.attack[2:]}-{args.benign[2:]}_y.png")

plt.figure(figsize=(20, 10))
plt.title(f"{args.file} -a {args.attack} -b {args.benign}")
plt.plot(pd_merged['timestamp'], pd_merged['atk_z'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_z'], color='green', label='benign')
# edit: show only 3 std range of data
# plt.xlim(0,60)
plt.axvline(x=20, color='black', linestyle='--')
plt.axvline(x=30, color='black', linestyle='--')
plt.axvline(x=50, color='black', linestyle='--')
plt.axvline(x=60, color='black', linestyle='--')
plt.axvline(x=60+20, color='black', linestyle='--')
plt.axvline(x=60+30, color='black', linestyle='--')
plt.axvline(x=60+50, color='black', linestyle='--')
plt.axvline(x=60+60, color='black', linestyle='--')
plt.axvline(x=120+20, color='black', linestyle='--')
plt.axvline(x=120+30, color='black', linestyle='--')
if args.marker == True:
    ymin = pd_merged['atk_x'].mean() - 3 * pd_merged['atk_x'].std()
    ymax = pd_merged['atk_x'].mean() + 3 * pd_merged['atk_x'].std()
    plt.vlines(x=pd_merged['mrk'], ymin=ymin, ymax = ymax, color='blue', linestyles='dotted')
plt.ylim(pd_merged['atk_z'].mean() - 3 * pd_merged['atk_z'].std(), pd_merged['atk_z'].mean() + 3 * pd_merged['atk_z'].std())
plt.legend(loc='upper right')
plt.xlabel('time [s]')
plt.ylabel('accel_z [m/s^2]')
plt.savefig(f"{args.file}-{args.attack[2:]}-{args.benign[2:]}_z.png")


# x-y plane plot
plt.figure(figsize=(10, 10))
plt.title(f"{args.file} -a {args.attack} -b {args.benign} X-Y plane")
plt.plot(pd_merged['ben_x'], pd_merged['ben_y'], color='green', label='benign')
plt.plot(pd_merged['atk_x'], pd_merged['atk_y'], color='red', label='attacked')
# TODO: plot points at 20,30,50,60,80,90 second of attacked data
# plt.scatter(pd_merged['atk_x'][20], pd_merged['atk_y'][20], color='black', marker='x')
""" atcked_datas = pd_merged.where(((pd_merged['timestamp'] >= 20) & (pd_merged['timestamp'] < 30))
                                | ((pd_merged['timestamp'] >= 50) & (pd_merged['timestamp'] < 60)
                                | ((pd_merged['timestamp'] >= 80) & (pd_merged['timestamp'] < 90)))).dropna()
plt.scatter(atcked_datas['atk_x'], atcked_datas['atk_y'], color='blue', marker='.', label='attacked') """
plt.legend(loc='upper right')
plt.xlabel('x [m/s^2]')
plt.ylabel('y [m/s^2]')
plt.savefig(f"{args.file}-{args.attack[2:]}-{args.benign[2:]}_xy.png")

# plt.show()
